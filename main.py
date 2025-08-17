import argparse
import sys
import os
from json_handler import JSONHandler
from logger import setup_logger, log_info


def main():
    """Main function with command-line interface"""
    parser = argparse.ArgumentParser(
        description="JSON Data Processing Tool - Validate, deduplicate, and process JSON data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input-file data.json --output-file processed.json
  %(prog)s --input-file data.json --output-file valid.json --log-file validation.log
        """
    )
    
    parser.add_argument(
        '--input-file',
        required=True,
        help='Input JSON file path'
    )
    
    parser.add_argument(
        '--output-file',
        required=True,
        help='Output JSON file path'
    )
    
    parser.add_argument(
        '--log-file',
        default='processing.log',
        help='Log file path (default: processing.log)'
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist")
        sys.exit(1)
    
    try:
        # Setup logger
        setup_logger(args.log_file)
        log_info(f"Starting JSON processing")
        log_info(f"Input file: {args.input_file}")
        log_info(f"Output file: {args.output_file}")
        log_info(f"Log file: {args.log_file}")
        
        # Initialize JSON handler
        handler = JSONHandler(args.input_file)
        
        # Perform validation
        log_info("Step 1: Validating records")
        validation_results = handler.validate_records()
        
        print(f"\nValidation Results:")
        print(f"Total records: {validation_results['total']}")
        print(f"Valid records: {validation_results['valid_count']}")
        print(f"Invalid records: {validation_results['invalid_count']}")
        
        # If there are invalid records, ask user what to do
        if validation_results['invalid_count'] > 0:
            print(f"\nWarning: {validation_results['invalid_count']} invalid records found.")
            response = input("Continue with only valid records? (y/n): ").lower().strip()
            if response != 'y':
                log_info("Process cancelled by user due to invalid records")
                print("Process cancelled.")
                return
            
            # Update handler data to only valid records
            handler.json_data = {'leads': validation_results['valid']}
            log_info(f"Updated data to {validation_results['valid_count']} valid records")
        
        # Perform deduplication
        log_info("Step 2: Deduplicating records")
        deduplicated_data = handler.de_duplicate()
        
        # Save final result
        handler.save_json(
            data=deduplicated_data,
            file_path=args.output_file,
            indent=2
        )
        
        # Print final summary
        final_count = len(deduplicated_data.get('leads', []))
        original_count = validation_results['total']
        removed_duplicates = original_count - final_count
        
        print(f"\nFinal Results:")
        print(f"Original records: {original_count}")
        print(f"Final records: {final_count}")
        print(f"Removed duplicates: {removed_duplicates}")
        print(f"Processed data saved to: {args.output_file}")
        
        log_info(f"Processing completed successfully")
        log_info(f"Final records: {final_count}")
        log_info(f"Data saved to: {args.output_file}")
        
    except Exception as e:
        error_msg = f"Error processing file: {str(e)}"
        # log_error(error_msg)
        print(f"Error: {error_msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
