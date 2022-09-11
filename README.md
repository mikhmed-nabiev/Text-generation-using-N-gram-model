### How to use
1. `$ python3 train.py --input-dir <path_to_data_dir> --model <path_to_model> ` <br /> 
Эта команда запустит процесс обучения. 
2. После того, как модель натренируется его надо запустить по следующей команде <br />
`$ python3 generate.py --model <path_to_model> --prefix <prefix_to_start> --length <length_of_text>` <br />
3. Если захотите начать сначал, то выполните команду <br />
 `$ python3 janitor.py --mode <path_to_model> `