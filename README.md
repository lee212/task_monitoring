# task_monitoring

## dependency

- pynvml
- psutil
- pandas
- numpy

## monitoring agent (data collector)

```
# Example on Summit
jsrun -nX -r1 -c1 -a1 python host.py \
                                     --times 720 \
                                     --interval 5 \
                                     --output_path $MEMBERWORK/bip109/task_monitoring/$RP_SESSION_ID/
```

## client monitoring (data loader)

```
python status.py --input_path $MEMBERWORK/bip109/task_monitoring/$RP_SESSION_ID/
```

## Ipython example

https://github.com/lee212/task_monitoring/blob/main/task_monitoring.ipynb
