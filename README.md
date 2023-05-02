# Battenburg_VIAS

Expermental tasks to study the visibility of the Battenburg pattern in trafic.
I removed the stimuli from the repository since they are not my property. I am
happy to provided more information if needed.

The structur I used for organising the project:
```
Battenburg
├── data
│   ├── cleaned <- data after clean_data.py
│   └── raw <- data before clean_data.py
├── docs
├── jspsych
├── scripts
├── stimuli
│   ├── car_prac <- stimuli for practice trials in offline photo task
│   ├── car_task <- stimuli for real trials in offline photo task
│   ├── clothes_prac <- stimuli for practice trials in online photo task
│   ├── clothes_task <- stimuli for real trials in online photo task
│   ├── film_prac <- stimuli for practice trials in offline film task
│   ├── film_task <- stimuli for real trials in offline film task
│   └── instructions_feedback <- images of instructions and feedback
├── .gitignore
├── LICENSE
└── README.md
```

## Offline car experiments

A reaction task to measure differences in speed between the Battenburg pattern
and the current police pattern in Belgium.

Make sure the stimuli are in `../Battenburg/stimuli/`, in the correct
directories. These are not included when downloading this repository. For
the real data collection, make sure to set fullscreen to `True`.

## Online clothes experiment

Online reaction time task to measure differences in speed between different
colours of the police uniform in Belgium.

The task is programmed in JavaScript and HTML with
[JsPsych](https://www.jspsych.org/7.3/). You will have to download JsPsych to
make it work.
