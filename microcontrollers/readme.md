# Microcontroller recruiting task

## What you are given
- 1 Nucleo board (STM32F446RE)
- 1 small board with a potentiometer, a voltage divider containing an NTC thermistor and a led.
- Some jumpers and wires to connect the boards together.

## Setting up the development environment

- Download STM32 CubeMX from the [official link](https://www.st.com/en/development-tools/stm32cubemx.html) and install it.
- Create a new project selecting the nucleo board you have been assigned.
- Once created the project, go to "Project Manager", fill out the project name, location and select "Makefile" as toolchain. Then go into code generator and assure that ```Generate peripheral initialization code in separate files``` is checked. Then click on "GENERATE CODE".

<img src="./media/cubemx_project.png" alt="drawing" width="900"/>
<img src="./media/cubemx_generator.png" alt="drawing" width="900"/>

- Open the generated folder in VsCode (you should see something like this).
- Install the platformio extension.

- Run `pio init` to generate the platformio project files, there is a sample configuration file provided in the [`platformio.ini`](./sample_platformio.ini) file, you can modify it if you need to. You can also use the `pio init --ide vscode` command to generate the project files for VsCode.

- Then run `pio update` to install the required packages and finally run `pio run` to build the project. If everything is set up correctly, you should see a message like this:

```
Advanced Memory Usage is available via "PlatformIO Home > Project Inspect"
RAM:   [          ]   0.4% (used 528 bytes from 131072 bytes)
Flash: [          ]   0.9% (used 4572 bytes from 524288 bytes)
Building .pio/build/release/firmware.bin
============================ [SUCCESS] Took 7.34 seconds ============================

Environment    Status    Duration
-------------  --------  ------------
release        SUCCESS   00:00:07.344
============================ 1 succeeded in 00:00:07.344 ============================
```

The project is now ready to be built and flashed to the board. You can use the `pio run -t upload` command to flash the firmware to the board. Check that with the `pio device list` command that the board is connected to your computer.

(NOTE: VsCode is not required, you can use any IDE of your choice, just install the PIO cli and use the commands above to build and flash the firmware).

### Wiring (to be changed)
| Label | Meaning        | Connection                  |
|-------|----------------|-----------------------------|
| VCC   | Power source   | Connect to 5V of system     |
| GND   | Ground         | Connect to GND of system    |
| DO    | Digital Output | Connect to digital IO pin   |
| AO    | Analog Output  | Connect to analog input pin |


## Prerequisites

![micropython meme](https://i.redd.it/yj4c5dzxurm81.jpg)

## The task

The task is divided in steps, each step is a milestone. Each step is given in logical and difficulty order. You will be graded on how many steps you complete and how well you implement them. You MUST commit your code FREQUENTLY to your git repository, as this will be used to evaluate your work. Implementing only the mandatory steps will NOT automatically mean that you will enter the next phase. Each candidate will be ranked based on the quality of their implementation and the number of steps completed. The best candidates will be invited to the next phase.

### Task

#### Step 1 (mandatory)

Your task is to read the NTC thermistor and the potentiometer, both in analog (using the ADC in DMA mode) and the digital value of the user button (using a GPIO input with interrupt), possibly apply some filters and send the data to serial. Then implement a small CLI with three commands:
- `raw`: remove all filters
- `moving average`: apply a moving average filter with 150 elements
- `random noise`: add artificial random noise <em>ad libitum</em>

You must control when the CLI is on and when it is off by using the button.

#### Step 2 (mandatory)

You will need to implement a small FSM (Finite State Machine) to control the behavior of the system (using the [libfsm-sw](https://github.com/eagletrt/libfsm-sw) library on the dev branch). The FSM should have the following states:
- <b>POST</b>. Power On Self Test, check if the sensors are working correctly. If not, go to the Error state. Else, go to the Waiting state.
- <b>Waiting</b>. The CLI is on, the board led is on and the external LED is off, sensor reading is off. If the button is pressed or the command `run` is received, go to the Listening state. While in the waiting state the external LED should have a breathing effect (PWM with period 2 seconds and duty cycle 0-100%). The breathing effect should be implemented using a timer peripheral. 
- <b>Listening</b>. The CLI is off and the board led is blinking with period 200ms duty cycle 80% (use a TIMER peripheral). Read the sensor, send via serial the data the same as in step 1. If the difference between the thermistor and potentiometer is greater than a predefined threshold for 5 seconds continuously, then go to the warning state otherwise if the button is pressed, go to the pause state. The external LED should indicate the difference of (thermistor - potentiometer) through PWM. The duty cycle should be 0% when the difference is 0 and 100% when the difference is greater than a predefined threshold.
- <b>Pause</b>. The CLI is on, the board led is blinking with period 2000 ms and duty cycle of 50% (use a TIMER peripheral), sensor reading is off. If the button is pressed or the command `run` is received, go to the Listening state. The external LED should have the same behavior as in the Waiting state.
- <b>Warning</b>. The CLI is off, the led is off, sensor reading is on. You must spam every 200 ms in serial "WARNING". If the button is pressed for more than 2 seconds, go to the Waiting state. If this state persists for more than 10 seconds, go to the Error state.
- <b>Error</b>. Any error you encounter will redirect you here (especially if HAL functions return anything different than HAL_OK). CLI is off, sensor reading is off, the led is blinking with period 40 ms and duty cycle 50% (use a TIMER peripheral). You must spam every 100 ms in serial "ERROR" explaining what error occured. The only way to exit this state is to reset the MCU by pressing the reset button.

#### Step 3 (mandatory)

Create unit tests for the modules you implemented. You must use the native environment of platformio to run the tests. You can use the [Unity](http://www.throwtheswitch.org/unity) framework for this purpose. (A sample configuration and test is provided in the `test` folder).

#### Step 4 (bonus)

Implement a simple serial interface on the host PC to receive the data from the MCU and plot it in real time. You can use any programming language you want. The data should also control the modulation of a sound signal (this part is intentionally vague, extra points for creative solutions).

#### Step 5 (bonus)

Use the timebase library to implement a simple scheduler that will allow you to run multiple tasks in parallel. You can use this to implement two separate FSMs, running their respective routines in two tasks, one for the sensor readings and one for the led control. Other FSM agnostic tasks can be implemented through this scheduler like serial communication and timer management.

#### Extra points

Every (reasonable) extra feature you implement cleanly and correctly will be evaluated and will give you extra points. Some examples of extra features are:
- Use vref to improve the ADC readings.
- Implement a CLI command to change the threshold for the warning state.
- Implement a CLI command to change the moving average filter size.
- Implement a CLI command to change the breathing effect period.
- Clean logging module with timestamps and log levels.
- Creativity will be rewarded within reason.

## Requirements

All code must follow standard code structure: ```./Core/Tests/``` for unit tests, ```./Core/Inc/``` for hardware specific header files, ```./Core/Inc/rec/``` for the hardware agnostic header files, ```./Core/Src/``` for hardware specific source files, ```./Core/Src/rec/``` for the hardware agnostic source files. Each module should have its own folder within these directories (a sample structure is shown in the image below). You can create additional folders if you need to, but the structure must be clear and easy to follow.

- Your code MUST follow the coding standards given in the [coding standards document](./standards.md). You will be evaluated on how well you follow the coding standards.
- Create a new GitHub repository, the repository name should be: ```embedded-project```.
- Create git commits as you make progress, THEY MUST BE FREQUENT AND DESCRIPTIVE [following standard naming](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13). You will be evaluated on your git history as well.
- All functions must be documented with Doxygen style comments. You can use the [Doxygen](https://www.doxygen.nl/) tool to generate documentation from your code.
- You must create a comprehensive README file that explains how to build and run your code, as well as how to use the CLI commands. The README file should also include a description of the FSM states and their transitions.

Example file structure:<br>
<img src="./media/example_filestructure.png" alt="drawing" height="600"/>
## Tips
- You have 2 full weeks of time to complete the task. Early submission will not be taken into account for evaluation so do not rush, take your time to implement the task correctly and cleanly. 
- Most of the cars boards code is public on the eagletrt organization on GitHub. Look at the dev branches of the repositories to see how the code is structured and how the coding standards are applied.
- Read this document again carefully and make sure you understand the requirements before starting to implement the task. We do not expect you to know everything about embedded programming, but we do expect you to be able to learn and apply new concepts quickly. Use the internet, forums, and documentation to your advantage.
- Be precise, you can do whatever you want that is not specified but we will be strict on the requirements that ARE specified.
- If you have any questions about the task please contact your recruiter, remember though that we are not technical support, we expect you to be able to solve problems on your own. We will only answer questions that are relevant to the task and that cannot be solved by reading the documentation or searching online.

## AI policy
**No AI generated code is allowed** in any way shape or form. You can use AI tools to help you understand concepts, but you must write the code yourself. Any code that is found to be generated by AI (or that you cannot explain yourself when asked) will be disqualified and you will not be invited to the next phase.
