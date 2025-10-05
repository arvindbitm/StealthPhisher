import re
import pandas as pd
from urllib.parse import urlparse
from url_complexity import *
from character_complexity import *
from fractinal_dimension import *
from kolmogorov_complexity import *
from detect_hexadecimal import *
from detect_base64 import *
from entropy import *
from bratio import *
from mRatio import *
from plqfa_new_feature import *
from linklyness import *
from unique_url import *

def OfflineCodeAnalyzer(WEBs):
    # Initialize feature variables
    NODES = {}
    equal, qmark, amp, digit, letter, specialchar = 0, 0, 0, 0, 0, 0
    LineOfCode, longestlinelen, selfhref, emptyref, extref, img, css, js, HasPopup, HasIFrame = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    # Decode and split web content into lines
    LINES = WEBs.decode('utf-8').split('\n')

    # Parse ID and URL from the first valid line
    valid_line = next((line for line in LINES if len(line.split()) >= 2 and line.split()[1].startswith("http")), None)
    if valid_line:
        id_part, OriginalURL = valid_line.split(maxsplit=1)
        NODES['ID'] = id_part
        NODES['URL'] = OriginalURL

        # URL Features
        urlLen = len(OriginalURL)
        NODES['LengthOfURL'] = urlLen
        domain = urlparse(OriginalURL).netloc
        NODES['Domain'] = domain
        NODES['URLComplexity'] = calculate_url_complexity(OriginalURL)
        NODES['CharacterComplexity'] = calculate_overall_ratio(OriginalURL)
        NODES['DomainLengthOfURL'] = len(domain)

        # Check if the domain is an IP address
        pattern = re.compile(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")
        NODES['IsDomainIP'] = 1 if pattern.match(domain) else 0

        # TLD Features
        TLD = domain.split('.')[-1] if '.' in domain else ''
        NODES['TLD'] = TLD
        NODES['TLDLength'] = len(TLD)

        # URL Character Features
        URL = OriginalURL.replace("https://", "").replace("http://", "").replace("www.", "")
        for ch in URL:
            if ch.isdigit():
                digit += 1
            elif ch.isalpha():
                letter += 1
            elif ch == '=':
                equal += 1
            elif ch == '?':
                qmark += 1
            elif ch == '%':
                amp += 1
            else:
                specialchar += 1

        NODES['LetterCntInURL'] = letter
        NODES['URLLetterRatio'] = round(letter / urlLen, 3)
        NODES['DigitCntInURL'] = digit
        NODES['URLDigitRatio'] = round(digit / urlLen, 3)
        NODES['EqualCharCntInURL'] = equal
        NODES['QuesMarkCntInURL'] = qmark
        NODES['AmpCharCntInURL'] = amp
        NODES['OtherSpclCharCntInURL'] = specialchar
        NODES['URLOtherSpecialCharRatio'] = round((equal + qmark + amp + specialchar) / urlLen, 3)

        # Additional URL Features
        NODES['NumberOfHashtags'] = number_of_hashtags(OriginalURL)
        NODES['NumberOfSubdomains'] = number_of_subdomains(OriginalURL)
        NODES['HavingPath'] = having_path(OriginalURL)
        NODES['PathLength'] = path_length(OriginalURL)
        NODES['HavingQuery'] = having_query(OriginalURL)
        NODES['HavingFragment'] = having_fragment(OriginalURL)
        NODES['HavingAnchor'] = having_anchor(OriginalURL)
        NODES['HasSSL'] = 1 if OriginalURL.startswith("https") else 0
    else:
        # Return empty if no valid URL found
        return {}

    # Initialize additional NODES attributes
    NODES.update({
        'IsUnreachable': 0, 'LineOfCode': 0, 'LongestLineLength': 0, 'HasTitle': 0,
        'TitleMatchScore': 0, 'HasFavicon': 0, 'HasRobotsBlocked': 0,
        'IsResponsive': 0, 'IsURLRedirects': 0, 'IsSelfRedirects': 0, 'HasDescription': 0,
        'HasPopup': 0, 'HasIFrame': 0, 'IsFormSubmitExternal': 0, 'HasSocialMediaPage': 0,
        'HasSubmitButton': 0, 'HasHiddenFields': 0, 'HasPasswordFields': 0, 'HasBankingKey': 0,
        'HasPaymentKey': 0, 'HasCryptoKey': 0, 'HasCopyrightInfoKey': 0
    })

    # Analyze HTML content line-by-line
    for LINE in LINES:
        try:
            LINE = LINE.lower()
            longestlinelen = max(longestlinelen, len(LINE))
            LineOfCode += 1

            # Remove spaces for certain checks
            LINE = LINE.replace(' ', '')

            # Check for redirection
            if 'redirectingto' in LINE:
                NODES['IsURLRedirects'] = 1

            # Check for IsUnreachable conditions
            if any(keyword in LINE for keyword in ['forbidden', 'accessdenied', 'invalidurl', 'servererror', 'humanverification', 'movedpermanently']):
                NODES['IsUnreachable'] = 1

            # Check for hyperlinks
            if 'href' in LINE:
                if 'http' in LINE:
                    extref += 1
                elif '="#"' in LINE:
                    emptyref += 1
                if domain in LINE or '="/' in LINE:
                    selfhref += 1

            # Cnt specific HTML elements
            if any(ext in LINE for ext in ['.jpg', '.jpeg', '.png']):
                img += 1
            if '.css' in LINE:
                css += 1
            if '.js' in LINE:
                js += 1
            if 'window.open' in LINE:
                HasPopup += 1
            if 'iframe' in LINE:
                HasIFrame += 1

            # Check for social network links and sensitive keywords
            if any(social in LINE for social in ['www.facebook.com', 'www.linkedin', 'www.youtube', 'www.twitter.com']):
                NODES['HasSocialMediaPage'] = 1
            if any(bank_term in LINE for bank_term in ['bank', 'wallet']):
                NODES['HasBankingKey'] = 1
            if 'pay' in LINE:
                NODES['HasPaymentKey'] = 1
            if 'crypto' in LINE:
                NODES['HasCryptoKey'] = 1

        except Exception as ex:
            print(ex)

    # Store final metrics
    NODES['LineOfCode'] = LineOfCode
    NODES['LongestLineLength'] = longestlinelen
    NODES['CntImages'] = img
    NODES['CntFilesCSS'] = css
    NODES['CntFilesJS'] = js
    NODES['CntSelfHRef'] = selfhref
    NODES['CntEmptyRef'] = emptyref
    NODES['CntExternalRef'] = extref
    NODES['CntPopup'] = HasPopup
    NODES['CntIFrame'] = HasIFrame

    if 'OriginalURL' in locals():
        NODES['UniqueURLCnt'] = count_unique_links(OriginalURL)

    # Unique Features
    NODES['WAPBenign'] = get_bRatio(OriginalURL)
    NODES['WAPMalicious'] = get_mRatio(OriginalURL)
    NODES['ShannonEntropy'] = calculate_entropy(OriginalURL)
    NODES['FractalDimension'] = fractal_dimension(OriginalURL)
    NODES['KolmogorovComplexity'] = kolmogorov_complexity(OriginalURL)
    NODES['HexPatternCnt'] = detect_hexadecimal(OriginalURL)
    NODES['Base64PatternCnt'] = detect_base64(OriginalURL)
    NODES['LikelinessIndex'] = calculate_likelynessindex(domain)

    return NODES
