sleep 60s
tmux new-session -d -s IsBaramiOpen
tmux send-keys -t IsBaramiOpen "cd /home/pi/IsBaramiOpen" C-m
tmux send-keys -t IsBaramiOpen "python3 readGyro.py" C-m
