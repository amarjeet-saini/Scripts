# Scripts

Contains some scripts :- <br/>
1. <h5>accuracy.py </h5> calculating accuracy if input file contains classes for actual and predict. <br/>
   Input file format : <br/>
   <img src="inputfile_for_accuracy.png"  width="128" height="200"/> <br/>
   <h6>Run:</h6> <h6>$ python3 accuracy.py filename.txt engine_no model_name TOTAL_CLASS </h6> <br/>
   model_name : any string <br/>
   TOTAL_CLASS :- any int i.e 5000 (for Imagenet)  <br/> 
   Output file format : .txt file bool {True: if correct prediction else False} <br/>

2. <h5>accuracy.py </h5> calculating no of mispredictions across 2 engine files. <br/>
   Input file format : 2 output files generated from parse script <br/>
                       [Actual | Predict]
                       
