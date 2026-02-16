from pathlib import Path
import re

p = Path('data_analysis.py')
txt = p.read_text(encoding='utf-8')

# Ensure outputs folder exists
if "os.makedirs('outputs'" not in txt and 'os.makedirs("outputs"' not in txt:
    if 'import matplotlib.pyplot as plt' in txt:
        txt = txt.replace(
            'import matplotlib.pyplot as plt',
            "import matplotlib.pyplot as plt\nimport os\nos.makedirs('outputs', exist_ok=True)"
        )
    else:
        txt = "import os\nos.makedirs('outputs', exist_ok=True)\n" + txt

# Replace every plt.show() with: save unique filename + show
# Unique filename uses an incrementing counter _figsave_i
if "_figsave_i" not in txt:
    insert = "\n_figsave_i = 1\n"
    # put counter right after matplotlib import (best place)
    if 'import matplotlib.pyplot as plt' in txt:
        txt = txt.replace('import matplotlib.pyplot as plt', 'import matplotlib.pyplot as plt' + insert)
    else:
        txt = insert + txt

replacement = (
    "plt.tight_layout()\n"
    "plt.savefig(f'outputs/figure_{_figsave_i}.png', dpi=200)\n"
    "_figsave_i += 1\n"
    "plt.show()"
)

# Only patch if we haven't already patched shows
if "figure_{_figsave_i}" not in txt:
    txt = txt.replace("plt.show()", replacement)

p.write_text(txt, encoding='utf-8')
print('✅ Patched data_analysis.py to save ALL figures into outputs/ as figure_1.png, figure_2.png, ...')
