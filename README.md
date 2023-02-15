# voicing_experiment_Chicago_prototype
simple experiment routine for voicing experiment

output_files = folder that saves the timing information of the trials
stimuli_images = folder that continues still images of start and move postures (will need to replace with sitting examples)
simuli_lists = where your stimulilists with random presentations live (as produced by the scrip generate_stimulist)
stimuli_videos =  this contains video examples of the movements which will help participants do the movements (wille need to be replaced with sitting trials)

generate_stimuli_lists.py = this creates a stimulilist for a particular participant number. If this is not generated first for a participant than the experiment script does not work
                            Note, that in the current case it just randomizes the movements for a number of predifined repetitions.

start_experiment1x = this runs the basic experiment, asks for a participant number (which will match it up with your generated stimulilist), and then you can run through the experiment
