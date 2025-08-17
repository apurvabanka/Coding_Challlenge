import json
from datetime import datetime
from logger import setup_logger, log_info, log_change
from model import UserModel
from pydantic import ValidationError


class JSONHandler:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.json_data = self.load_json()
        # Setup logger for deduplication
        setup_logger("deduplication.log")

    def load_json(self):
        """
        Load JSON data from a file
        
        Returns:
            dict: JSON data loaded from the file
        """
        with open(self.json_file_path, 'r') as file:
            return json.load(file)

    def save_json(self, data=None, file_path=None, indent=2):
        """
        Save JSON data to a file
        
        Args:
            data: JSON data to save (if None, uses self.json_data)
            file_path: Path to save the file (if None, uses self.json_file_path)
            indent: Number of spaces for indentation (default: 2)
        """
        if data is None:
            data = self.json_data
        
        if file_path is None:
            file_path = self.json_file_path
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=indent, ensure_ascii=False)

    def validate_records(self):
        """
        Validate every record in the JSON data using the UserModel.
        
        Returns:
            dict: Validation results with valid and invalid records
        """
        log_info("Starting record validation process")
        
        if 'leads' not in self.json_data:
            log_info("No 'leads' key found in JSON data")
            return {"valid": [], "invalid": [], "total": 0}
        
        leads = self.json_data['leads']
        total_records = len(leads)
        log_info(f"Validating {total_records} records")
        
        valid_records = []
        invalid_records = []
        validation_errors = {}
        
        for i, record in enumerate(leads):
            try:
                # Map _id to id for Pydantic validation
                validation_record = record.copy()
                if '_id' in validation_record:
                    validation_record['id'] = validation_record.pop('_id')
                
                # Validate the record using UserModel
                validated_record = UserModel(**validation_record)
                
                # Convert back to original format for output
                output_record = validated_record.model_dump()
                if 'id' in output_record:
                    output_record['_id'] = output_record.pop('id')
                
                valid_records.append(output_record)
                log_info(f"Record {i+1} (ID: {record.get('_id', 'unknown')}) - VALID")
                
            except ValidationError as e:
                # Record is invalid, collect error details
                error_details = []
                for error in e.errors():
                    field = error['loc'][0] if error['loc'] else 'unknown'
                    # Map 'id' back to '_id' in error messages
                    if field == 'id':
                        field = '_id'
                    message = error['msg']
                    error_details.append(f"{field}: {message}")
                
                invalid_records.append(record)
                validation_errors[i] = error_details
                
                log_change("Record validation failed", 
                          value_from=f"Record {i+1} (ID: {record.get('_id', 'unknown')})", 
                          value_to="INVALID", 
                          additional_info=f"Errors: {', '.join(error_details)}")
        
        # Log validation summary
        valid_count = len(valid_records)
        invalid_count = len(invalid_records)
        
        log_info(f"Validation completed: {valid_count} valid, {invalid_count} invalid out of {total_records} records")
        
        if invalid_count > 0:
            log_info(f"Invalid records found: {invalid_count} records have validation errors")
            for i, errors in validation_errors.items():
                record_id = leads[i].get('_id', 'unknown')
                log_info(f"Record {i+1} (ID: {record_id}) errors: {', '.join(errors)}")
        
        return {
            "valid": valid_records,
            "invalid": invalid_records,
            "validation_errors": validation_errors,
            "total": total_records,
            "valid_count": valid_count,
            "invalid_count": invalid_count
        }

    def de_duplicate(self):
        """
        Remove duplicates from JSON data based on _id and email.
        Prefers newest date, and for identical dates, prefers the last record in the list.
        
        Returns:
            dict: Deduplicated and sorted JSON data
        """
        log_info("Starting deduplication process")
        
        if 'leads' not in self.json_data:
            log_info("No 'leads' key found in JSON data")
            return self.json_data
        
        leads = self.json_data['leads']
        original_count = len(leads)
        log_info(f"Processing {original_count} records")
        
        # Track duplicates by _id and email
        id_records = {}  # _id -> list of records
        email_records = {}  # email -> list of records
        
        # Group records by _id and email
        for i, record in enumerate(leads):
            record_id = record.get('_id')
            email = record.get('email')
            
            if record_id:
                if record_id not in id_records:
                    id_records[record_id] = []
                id_records[record_id].append((i, record))
            
            if email:
                if email not in email_records:
                    email_records[email] = []
                email_records[email].append((i, record))
        
        # Find records to keep (no duplicates)
        records_to_keep = set()
        duplicates_removed = 0
        
        # Process _id duplicates
        for record_id, records in id_records.items():
            if len(records) > 1:
                log_info(f"Found {len(records)} records with duplicate _id: {record_id}")
                
                sorted_records = sorted(records, key=lambda x: x[0])  # Sort by index to maintain order
                keep_index, keep_record = sorted_records[-1]  # Keep the last one (highest index)
                records_to_keep.add(keep_index)
                
                # Log the kept record
                kept_date = keep_record.get('entryDate', 'unknown')
                log_change("Kept record with duplicate _id", 
                          value_from=f"index {sorted_records[0][0]}", 
                          value_to=f"index {keep_index}", 
                          additional_info=f"kept last occurrence: {kept_date}")
                
                duplicates_removed += len(records) - 1
            else:
                # No duplicates, keep the record
                records_to_keep.add(records[0][0])
        
        # Process email duplicates
        for email, records in email_records.items():
            if len(records) > 1:
                log_info(f"Found {len(records)} records with duplicate email: {email}")
                
                # Simply keep the last record in the list (highest index)
                # This maintains the original order and keeps the latest occurrence
                sorted_records = sorted(records, key=lambda x: x[0])  # Sort by index to maintain order
                keep_index, keep_record = sorted_records[-1]  # Keep the last one (highest index)
                records_to_keep.add(keep_index)
                
                # Log the kept record
                kept_date = keep_record.get('entryDate', 'unknown')
                log_change("Kept record with duplicate email", 
                          value_from=f"index {sorted_records[0][0]}", 
                          value_to=f"index {keep_index}", 
                          additional_info=f"kept last occurrence: {kept_date}")
                
                duplicates_removed += len(records) - 1
            else:
                # No duplicates, keep the record
                records_to_keep.add(records[0][0])
        
        # Create deduplicated list maintaining original order
        deduplicated_leads = []
        for i in sorted(records_to_keep):
            deduplicated_leads.append(leads[i])
        
        # Update the JSON data
        self.json_data['leads'] = deduplicated_leads
        
        final_count = len(deduplicated_leads)
        log_info(f"Deduplication completed: {original_count} -> {final_count} records")
        log_info(f"Removed {duplicates_removed} duplicate records")
        
        return self.json_data