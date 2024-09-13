. .\variables.ps1
wt -w 0 nt --title "CLIENT 01" --tabColor "#00FFF3" -p powershell -d $folder_path\client\ -c python main.py
wt -w 0 nt --title "CLIENT 02" --tabColor "#B200FF" -p powershell -d $folder_path\client\ -c python main.py
