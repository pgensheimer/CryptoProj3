# CryptoProj3
repository for crypto project "File Locker"

Everything was successfully implemented except in part 4. We could not get rsa-enc to work with the aeskey. Rather than not get the project done, we implemented a workaround where we put the aeskey in a separate file unencrypted which could later be verified with a tag. The one other thing that doesn't work is we couldn't use cbc-mactag on the encrypted bytes due to problems with understanding bytestrings. Our workaround for this was tagging the plaintext files instead. The program encrypts and decrypts files successfully. We understand we missed some specifications. However, our knowledge of using python with bytes was very limited and prevented us from fully implemented said specifications.
