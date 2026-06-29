$file = "d:\1. BDS\AI-Assistant\App_kham_benh_tai_san\index.html"
$c = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

# Fix 1: escaped quotes \'%\' -> '%' and corrupted em-dash
# Pattern: \'%\' and \'â€"\'
$c = $c.Replace("\'%\'", "'%'")
$c = $c.Replace("\'â€"\'", "'—'")

# Also fix any remaining backslash-quote pairs that are invalid JS
$c = $c.Replace("\\\'", "'")

[System.IO.File]::WriteAllText($file, $c, [System.Text.Encoding]::UTF8)
Write-Host "Fixed! Size: $((Get-Item $file).Length) bytes"

# Verify
$check = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)
if ($check.Contains("\'%\'") -or $check.Contains("\\\'")) {
    Write-Host "WARNING: Still has escaped quotes!"
} else {
    Write-Host "OK: No more escaped quotes found."
}
