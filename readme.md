## Installation   
Just use `git clone https://github.com/YaokaiYang-assaultmaster/Python-based-RTT-hop-distance-and-geo-distance-measurer` to pull the codes to your local directory. 

## Usage
After clone, change directory to the pulled directory. 

1. distMeasurement.py is used to calculate the hop distance and RTT between 10 given destination host in targets.txt. 

2. geoMeasurement.py is used to calculate the geographical distance between this computer to the destination hosts listed in targets.txt using the web-based service. 

3. targets.txt list is the list of websites that is going to be tested. 

4. The execution method is:    
```sudo python distMeasurement.py```   
```python geoDistance.py```   

5. The `targets.txt` and python programs need to be stored in the same directory. 
