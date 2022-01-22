# Scripts

Contains some scripts for accuracy calculation and parsing:- <br/>
1. [accuracy.py](https://github.com/amarjeet-saini/Scripts/blob/main/accuracy.py)</br>
   calculating accuracy if input file contains classes for actual and predict. <br/>
   <h6>Run :</br> $ python3 accuracy.py filename.txt engine_no model_name TOTAL</h6>
   model_name : any string <br/>
   TOTAL :- no of images inference set any int i.e 5000 (for Imagenet)  <br/> 
   <h5>Input file format :</h5>
   <img src="inputfile_for_accuracy.png"  width="128" height="200"/> 
   <h5>Output file format :</h5> .txt file bool {True: if correct prediction else False} <br/>

2. [mispredict_engines.py](https://github.com/amarjeet-saini/Scripts/blob/main/mispredict_engines.py)</br>
   calculating no of mispredictions across output files of 2 engine. <br/>
   <h6>Run :</br> $ python3 mispredict_engines.py output1.txt output2.txt</h6>
   <h5>Input file format :</h5> 2 output files generated from parse script <br/>
                       [Actual | Predict]
                       
   <h5>Output :</h5> return # of misprediction out of TOTAL
