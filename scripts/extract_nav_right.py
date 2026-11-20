with open('scripts/v1_header.html', 'r', encoding='utf-8') as f:
    hdr = f.read()

import re
right_match = re.search(r'<div class="nav-right[\s\S]*?</div>\s*</div>\s*</header>', hdr)
if right_match:
    print(right_match.group(0))
else:
    # search for nav-right
    right_match2 = re.search(r'class="[^"]*nav-right[^"]*"[\s\S]*?</header>', hdr)
    if right_match2:
        print(right_match2.group(0))
    else:
        print("Not found, last 1000 chars:")
        print(hdr[-1000:])
