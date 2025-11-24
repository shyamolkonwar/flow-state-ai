#!/bin/bash

# Add license, contact, and acknowledgments sections to all .md files in docs/

LICENSE_TEXT='## License

This software is proprietary and all rights are reserved by Shyamol Konwar. No part of the software may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of Shyamol Konwar.

The software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall Shyamol Konwar be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

For licensing inquiries, please contact Shyamol Konwar.

## Contact

Email: shyamol@fusionfocus.in
Website: https://fusionfocus.in

## Acknowledgments

Built for students and knowledge workers who want to achieve deeper, more sustained focus in an increasingly distracting digital world.

---

**No contributions needed. This software is fully licensed and proprietary.**'

# Find all .md files in docs/ directory
find docs -name "*.md" -type f | while read -r file; do
    echo "Processing $file..."
    
    # Check if file already has license section
    if grep -q "## License" "$file"; then
        echo "  Already has license section, skipping"
        continue
    fi
    
    # Add the license text at the end of the file
    echo "" >> "$file"
    echo "$LICENSE_TEXT" >> "$file"
    
    echo "  Added license section"
done

echo "Done!"
