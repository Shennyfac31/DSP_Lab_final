# DSP_Lab_final
[final.py](final.py)是main，跑它的話會讓你錄十次音（錄的次數可以改for的參數決定）。但你錄的音不會存檔，會直接被拿去test，然後印出它判斷的結果（括號前面的數字：1:up, 2:down, 3:left, 4:right, 5:hit。括號後面的數字：DTW的距離）。

[record_temp.py](record_temp.py)是錄音用的。錄的音會存在[train](train/)裡面。錄的時候記得改檔名不然會被rewrite喔。

錄完音之後如果要load你的template，可以改[recognition.py](recognition.py)中的function。可以用feat2存你的template。底下test function DTW的部分也要改一下。

在跑[final.py](final.py)和[record_temp.py](record_temp.py)時，有時會有點秀逗XD。就是錄太久或太快。先警告一下XP

如果真的怕它錄太久，可以改[get_voice.py](get_voice.py)。只要uncomment第67,68行，就只會最多錄五秒。

>Uncomment:   
>
>        #if frames.size>RATE*5:   
>        #    stop = 1   
