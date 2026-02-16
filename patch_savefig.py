from pathlib import Path

p = Path('data_analysis.py')
txt = p.read_text(encoding='utf-8')

# Ensure outputs folder creation is in the script
if "os.makedirs('outputs'" not in txt and 'os.makedirs("outputs"' not in txt:
    if 'import matplotlib.pyplot as plt' in txt:
        txt = txt.replace('import matplotlib.pyplot as plt',
                          "import matplotlib.pyplot as plt\nimport os\nos.makedirs('outputs', exist_ok=True)")
    else:
        txt = "import os\nos.makedirs('outputs', exist_ok=True)\n" + txt

# Replace each plt.show() with save + show (only if not already saving)
if "plt.savefig('outputs/" not in txt and 'plt.savefig("outputs/' not in txt:
    txt = txt.replace('plt.show()',
                      "plt.tight_layout()\nplt.savefig(f'outputs/figure_{plt.gcf().number}.png', dpi=200)\nplt.show()")

p.write_text(txt, encoding='utf-8')
print('✅ Patched data_analysis.py to save figures into outputs/')
