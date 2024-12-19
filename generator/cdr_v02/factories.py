import random

class MSISDNFactory:
    @staticmethod
    def generate(msisdn_type: str, country_code=None, ndc=None, prefix=None, digits=6) -> str:
        """
        Generates an MSISDN based on the type and provided parameters.

        Args:
            msisdn_type (str): Type of MSISDN ('local', 'national', 'international').
            country_code (str): The country code for 'local' or 'national' types.
            ndc (int, list, or tuple): A single NDC or a range of NDCs for 'local' or 'national' types.
            prefix (list): List of valid prefixes for 'international' type.
            digits (int, optional): Number of digits for the subscriber number. Defaults to 6.

        Returns:
            str: The generated MSISDN.

        Raises:
            ValueError: If msisdn_type is invalid or required parameters are missing.
        """
        try:
            if digits < 1:
                raise ValueError("The 'digits' parameter must be a positive integer.")

            if msisdn_type in ("home", "national"):
                if not country_code or ndc is None:
                    raise ValueError("'country_code' and 'ndc' are required for 'home' or 'national' types.")

                # Determine the NDC value
                if isinstance(ndc, int):
                    ndc_value = ndc  # Use the single integer as the NDC
                elif isinstance(ndc, (list, tuple)) and len(ndc) == 2:
                    ndc_value = random.randint(ndc[0], ndc[1])  # Random NDC within the range
                else:
                    raise ValueError("'ndc' must be an integer or a range (list/tuple) with two values.")

                subscriber_number = random.randint(10**(digits - 1), 10**digits - 1)  # Random subscriber number
                return f"{country_code}{ndc_value}{subscriber_number}"

            elif msisdn_type == "international":
                if not prefix:
                    raise ValueError("'prefix' is required for 'international' type.")

                selected_prefix = random.choice(prefix)  # Randomly select a prefix
                subscriber_number = random.randint(10**(digits - 1), 10**digits - 1)  # Random subscriber number
                return f"{selected_prefix}{subscriber_number}"

            else:
                raise ValueError(f"Invalid msisdn_type: {msisdn_type}")
        except ValueError as e:
            return f"Error generating MSISDN: {str(e)}"


class IMSIFactory:
    @staticmethod
    def generate() -> str:
        """
        Generates a valid IMSI (International Mobile Subscriber Identity).

        Returns:
            str: The generated IMSI.
        """
        try:
            mcc = f"{random.randint(100, 999):03d}"  # Ensure 3 digits
            mnc = f"{random.randint(0, 999):03d}"   # Ensure 3 digits, with leading zeros if needed
            msin = f"{random.randint(0, 999999999):09d}"  # Ensure 9 digits, with leading zeros if needed
            return f"{mcc}{mnc}{msin}"
        except Exception as e:
            return f"Error generating IMSI: {str(e)}"


class IMEIFactory:
    @staticmethod
    def generate() -> str:
        """
        Generates a valid IMEI (International Mobile Equipment Identity) number.

        Returns:
            str: The generated IMEI.
        """
        try:
            # Generate the first 14 digits of the IMEI
            imei = [str(random.randint(0, 9)) for _ in range(14)]

            # Calculate the Luhn checksum digit
            total_sum = 0
            for i in range(14):
                digit = int(imei[i])
                if i % 2 == 1:  # Double every second digit
                    digit *= 2
                    if digit > 9:  # If doubling results in two digits, subtract 9
                        digit -= 9
                total_sum += digit

            # Compute the check digit
            check_digit = (10 - (total_sum % 10)) % 10
            imei.append(str(check_digit))

            # Return the full IMEI as a string
            return ''.join(imei)
        except Exception as e:
            return f"Error generating IMEI: {str(e)}"



class MSISDNFactory:
    @staticmethod
    def generate(msisdn_type: str, country_code: str, ndc: list, prefix: list = None, digits: int = 6) -> str:
        """Generate a random MSISDN based on the given type and configuration."""
        if msisdn_type in ["home", "national"]:
            # Use a random NDC range and generate the remaining digits
            ndc_start, ndc_end = random.choice(ndc)
            msisdn = f"{country_code}{random.randint(ndc_start, ndc_end):0{digits}d}"
        elif msisdn_type == "international":
            # Use a random prefix and generate the remaining digits
            msisdn = f"{random.choice(prefix)}{random.randint(10**(digits-1), 10**digits - 1)}"
        else:
            raise ValueError(f"Invalid MSISDN type: {msisdn_type}")
        return msisdn

