#Local
mainAddr = 0x134c
winAddr = 0x12aa
offset = mainAddr - winAddr

#Remote
main_remote = 0x562c9a78334c
win_remote = main_remote-offset
print(hex(win_remote))  
