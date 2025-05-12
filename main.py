import argparse
import base64
import hashlib
import logging
import random
import sys
from typing import List, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataTypeConverter:
    """
    Converts data from one format to another for data masking purposes.
    """

    def __init__(self):
        """
        Initializes the DataTypeConverter.
        """
        pass

    def to_hex(self, data: Union[int, str]) -> str:
        """
        Converts an integer or string to its hexadecimal representation.

        Args:
            data: The integer or string to convert.

        Returns:
            The hexadecimal representation of the input data.

        Raises:
            TypeError: If the input data is not an integer or string.
            ValueError: If the string cannot be converted to bytes properly (encoding issues).
        """
        try:
            if isinstance(data, int):
                return hex(data)
            elif isinstance(data, str):
                return data.encode('utf-8').hex()  # Encode to bytes first
            else:
                raise TypeError("Input must be an integer or string.")
        except ValueError as e:
            logging.error(f"Error converting to hex: {e}")
            raise
        except Exception as e:
            logging.exception(f"Unexpected error during hex conversion: {e}")
            raise

    def to_base64(self, data: str) -> str:
        """
        Converts a string to its base64 encoded representation.

        Args:
            data: The string to convert.

        Returns:
            The base64 encoded string.

        Raises:
            TypeError: If the input data is not a string.
            ValueError: If encoding fails.
        """
        if not isinstance(data, str):
            raise TypeError("Input must be a string.")
        try:
            data_bytes = data.encode('utf-8')  # Encode to bytes
            base64_bytes = base64.b64encode(data_bytes)
            return base64_bytes.decode('utf-8')
        except ValueError as e:
            logging.error(f"Error converting to base64: {e}")
            raise
        except Exception as e:
            logging.exception(f"Unexpected error during base64 conversion: {e}")
            raise

    def to_md5(self, data: str) -> str:
      """
      Converts a string to its MD5 hash representation.  MD5 is considered cryptographically broken and should not be used for security purposes, only masking.

      Args:
          data: The string to convert.

      Returns:
          The MD5 hash of the input string.

      Raises:
          TypeError: If the input data is not a string.
      """
      if not isinstance(data, str):
          raise TypeError("Input must be a string.")
      try:
          data_bytes = data.encode('utf-8')
          md5_hash = hashlib.md5(data_bytes).hexdigest()
          return md5_hash
      except Exception as e:
          logging.exception(f"Unexpected error during MD5 hash generation: {e}")
          raise

    def randomly_convert(self, data: str) -> str:
        """
        Randomly selects a conversion method (to_hex, to_base64, to_md5) and applies it to the input data.

        Args:
            data: The string to convert.

        Returns:
            The converted string.

        Raises:
            TypeError: If the input data is not a string.
        """
        if not isinstance(data, str):
            raise TypeError("Input must be a string.")
        methods = [self.to_hex, self.to_base64, self.to_md5]
        chosen_method = random.choice(methods)
        try:
            return chosen_method(data)
        except Exception as e:
            logging.error(f"Error during random conversion using {chosen_method.__name__}: {e}")
            raise


def setup_argparse() -> argparse.ArgumentParser:
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        An argparse.ArgumentParser object.
    """
    parser = argparse.ArgumentParser(description="Converts data from one format to another for data masking.")
    parser.add_argument("data", help="The data to convert.")
    parser.add_argument("-m", "--method", choices=["hex", "base64", "md5", "random"], default="random",
                        help="The conversion method to use (hex, base64, md5, or random).  Defaults to random.")
    return parser


def main() -> None:
    """
    The main function that parses arguments, performs the data conversion, and prints the result.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    converter = DataTypeConverter()

    try:
        if args.method == "hex":
            #Handles both string and int input
            try:
              data = int(args.data)
            except ValueError:
              data = args.data
            converted_data = converter.to_hex(data)
        elif args.method == "base64":
            converted_data = converter.to_base64(args.data)
        elif args.method == "md5":
            converted_data = converter.to_md5(args.data)
        else:  # random
            converted_data = converter.randomly_convert(args.data)

        print(f"Converted data: {converted_data}")

    except TypeError as e:
        logging.error(f"Type error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)  # Non-zero exit code indicates an error
    except ValueError as e:
        logging.error(f"Value error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")  # Log the full stack trace
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()