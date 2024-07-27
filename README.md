### Requirements 

⚠️⚠️ Make sure your python version is > 3.10.0 ⚠️⚠️

Sample audio available at `data/test_samles/fake-0.mp3`

```
pip install -r requirements.txt
```

Run the api.py 

```
python api.py

```

Access API Docs:

```
http://0.0.0.0:9999/docs#/

```

## Training 

### training_run

This model is a fine-tuned version of [NumbersStation/nsql-350M](https://huggingface.co/NumbersStation/nsql-350M) on an custom dataset.



### Using this model
Install PEFT:
```
pip install peft

```

```
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM

config = PeftConfig.from_pretrained("Rajan/training_run")
base_model = AutoModelForCausalLM.from_pretrained("NumbersStation/nsql-350M")
model = PeftModel.from_pretrained(base_model, "Rajan/training_run")

```

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->


### Training procedure

#### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 0.0001
- train_batch_size: 8
- eval_batch_size: 8
- seed: 42
- gradient_accumulation_steps: 2
- total_train_batch_size: 16
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: linear
- num_epochs: 2

#### Training results

**Loss Per Step**

![](training/loss.png)


### Testing Results


| Metric | Value |
| --- | --- |
| Precision | 0.9174434087882823 |
| Recall | 0.7162162162162162 |
| F1 Score | 0.804436660828955 |
| Accuracy | 0.7162162162162162 |

#### Framework versions

- PEFT 0.12.0
- Transformers 4.42.3
- Pytorch 2.1.2
- Datasets 2.20.0
- Tokenizers 0.19.1

