# Fonts

Both families are bundled rather than fetched, so the app renders correctly offline and the first frame has no font swap.

| File | Source | Licence |
| --- | --- | --- |
| `PlusJakartaSans-{Regular,Medium,SemiBold,Bold}.ttf` | Static builds from the upstream project, [tokotype/PlusJakartaSans](https://github.com/tokotype/PlusJakartaSans), version 2.071. Unmodified | SIL OFL 1.1, `OFL-PlusJakartaSans.txt` |
| `Lora.ttf`, `Lora-Italic.ttf` | Google Fonts, `ofl/lora/Lora[wght].ttf` and `Lora-Italic[wght].ttf`, version 3.008. Unmodified, renamed only | SIL OFL 1.1, `OFL-Lora.txt` |

**Lora is shipped as Google's variable file without modification.** Its licence reserves the font name "Lora", so a modified copy, such as a static weight cut from the variable file, could not be called Lora. The app only uses weight 400, which is the variable file's default instance, so no modification is needed. If a heavier Lora weight is ever wanted, use the variable file's weight axis rather than cutting a new file.

Only the weights the design uses are included: Plus Jakarta Sans 400, 500, 600, 700, and Lora 400 regular and italic.

The SIL Open Font License requires its text to ship with the fonts, so both licence files travel with them into the app.
