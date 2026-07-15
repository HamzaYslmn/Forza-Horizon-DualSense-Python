# DSX Mod System
Mods allow you to send data to DSX via UDP communications to control things like Adaptive Triggers and LEDs connected to DSX.

**DSX v3.1+** supports the Legacy v2 Mod System while a new Mod System is being developed for v3. The upcoming Mod System will include advanced features like APIs and more.

## Quick Access

- [Reset To User Settings](#reset-to-user-settings)
- [Lightbar LED](#lightbar-led)
- [Player LED](#player-led)
- [Mic LED](#mic-led)
- [Trigger Threshold](#trigger-threshold)
- [Adaptive Triggers](#adaptive-triggers)
 - DSX v3.1+ Adaptive Trigger Modes
     - [OFF](#off)
     - [FEEDBACK](#feedback)
     - [WEAPON](#weapon)
     - [VIBRATION](#vibration)
     - [SLOPE_FEEDBACK](#slope_feedback)
     - [MULTIPLE_POSITION_FEEDBACK](#multiple_position_feedback)
     - [MULTIPLE_POSITION_VIBRATION](#multiple_position_vibration)
 - DSX v2 Adaptive Trigger Modes (LEGACY // Avoid Using)
     - [Normal](#normal)
     - [GameCube](#gamecube)
     - [VerySoft](#verysoft)
     - [Soft](#soft)
     - [Hard](#hard)
     - [VeryHard](#veryhard)
     - [Hardest](#hardest)
     - [Rigid](#rigid)
     - [VibrateTrigger](#vibratetrigger)
     - [Choppy](#choppy)
     - [Medium](#medium)
     - [VibrateTriggerPulse](#vibratetriggerpulse)
     - [CustomTriggerValue](#customtriggervalue)
     - [Resistance](#resistance)
     - [Bow](#bow)
     - [Galloping](#galloping)
     - [SemiAutomaticGun](#semiautomaticgun)
     - [AutomaticGun](#automaticgun)
     - [Machine](#machine)
     - [VIBRATE_TRIGGER_10Hz](#vibrate_trigger_10hz)


### Usage:
___________________
#### Multiple Instructions Sent Together
```cs
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddRGBToPacket(packet, controllerIndex, 255, 255, 255, 255);
packet = AddPlayerLEDToPacket(packet, controllerIndex, PlayerLEDNewRevision.One);
packet = AddMicLEDToPacket(packet, controllerIndex, MicLEDMode.Pulse);
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.GameCube, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Resistance, new List<int> { 0, 8 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________
#### Reset To User Settings
```cs
// When sent to DSX, it will discard any modifications
// sent to the controller and apply the settings from the profile it's attached to in DSX
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddResetToPacket(packet, controllerIndex);

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________
#### Lightbar LED
```cs
// Needs 4 Params in List<int> (Red: 0-255) (Green: 0-255) (Blue: 0-255) (Brightness: 0-255)
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddRGBToPacket(packet, controllerIndex, 255, 255, 255, 255);

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________
#### Player LED
```cs
// Layout for Player LEDs
// Needs 1 Param (PlayerLEDNewRevision: Enum)
//  - -x- -  Player 1
//  - x-x -  Player 2
//  x -x- x  Player 3
//  x x-x x  Player 4
//  x xxx x  Player 5
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddPlayerLEDToPacket(packet, controllerIndex, PlayerLEDNewRevision.One);

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________
#### Mic LED
```cs
// Three modes: ON, PULSE, or OFF
// Needs 1 Param (MicLEDMode: Enum)
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddMicLEDToPacket(packet, controllerIndex, MicLEDMode.Pulse);

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________
#### Trigger Threshold
```cs
// This is used for telling the emulation when to send the "pressed state"
// Needs 1 Param in List<int> (Threshold: 0-255)
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddTriggerThresholdToPacket(packet, controllerIndex, Trigger.Left, 0);
packet = AddTriggerThresholdToPacket(packet, controllerIndex, Trigger.Right, 0);

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

### Adaptive Triggers

___________________

### DSX v3.0+ Adaptive Trigger Modes
#### OFF
```cs
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.OFF, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.OFF, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### FEEDBACK
```cs
// Needs 2 Params in List<int> (Start Position: 1-9) -> (Resistance Strength: 1-8)
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.FEEDBACK, new List<int> { 1, 8 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.FEEDBACK, new List<int> { 1, 8 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### WEAPON
```cs
// Needs 3 Params in List<int> (Start Position: 2-7) -> (End Position: 3-8) -> (Resistance Strength: 1-8)
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.WEAPON, new List<int> { 2, 6, 8 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.WEAPON, new List<int> { 2, 6, 8 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### VIBRATION
```cs
// Needs 3 Params in List<int> (Start Position: 1-9) -> (Amplitude: 1-8) -> (Frequency: 1-40)
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.VIBRATION, new List<int> { 1, 8, 10 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.VIBRATION, new List<int> { 1, 8, 10 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### SLOPE_FEEDBACK
```cs
// Needs 4 Params in List<int> (Start Position: 1-8) -> (End Position: 2-9) -> (Start Resistance Strength: 1-8) -> (End Resistance Strength: 1-8)
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.SLOPE_FEEDBACK, new List<int> { 1, 9, 8, 1 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.SLOPE_FEEDBACK, new List<int> { 1, 9, 8, 1 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### MULTIPLE_POSITION_FEEDBACK
```cs
// Needs 10 Params in List<int> 10 Region Resistance Strength: (Region 1: 0-8) -> (Region 2: 0-8) -> (Region 3: 0-8) -> (Region 4: 0-8) -> (Region 5: 0-8) -> (Region 6: 0-8) -> (Region 7: 0-8) -> (Region 8: 0-8) -> (Region 9: 0-8) -> (Region 10: 0-8)
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.MULTIPLE_POSITION_FEEDBACK, new List<int> { 8, 8, 8, 0, 0, 0, 8, 8, 0, 0 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.MULTIPLE_POSITION_FEEDBACK, new List<int> { 8, 8, 8, 0, 0, 0, 8, 8, 0, 0 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### MULTIPLE_POSITION_VIBRATION
```cs
// Needs 11 Params in List<int> (Frequency: 1-40) -> 10 Region Amplitude: (Region 1: 0-8) -> (Region 2: 0-8) -> (Region 3: 0-8) -> (Region 4: 0-8) -> (Region 5: 0-8) -> (Region 6: 0-8) -> (Region 7: 0-8) -> (Region 8: 0-8) -> (Region 9: 0-8) -> (Region 10: 0-8)
// Usage ==============

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.MULTIPLE_POSITION_VIBRATION, new List<int> { 10, 8, 8, 8, 8, 8, 0, 0, 0, 8, 8 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.MULTIPLE_POSITION_VIBRATION, new List<int> { 10, 8, 8, 8, 8, 8, 0, 0, 0, 8, 8 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________
### DSX v2 Adaptive Trigger Modes (Legacy)
#### Normal
 ```cs
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.Normal, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Normal, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### GameCube
```cs
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.GameCube, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.GameCube, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### VerySoft
```cs
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.VerySoft, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.VerySoft, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### Soft
```cs
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.Soft, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Soft, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### Hard
```cs
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.Hard, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Hard, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### VeryHard
```cs
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.VeryHard, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.VeryHard, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### Hardest
```cs
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.Hardest, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Hardest, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### Rigid
```cs
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.Rigid, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Rigid, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### VibrateTrigger
```cs
// Needs 1 Param in List<int> (Frequency: 0-255)
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.VibrateTrigger, new List<int> { 10 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.VibrateTrigger, new List<int> { 10 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### Choppy
```cs
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.Choppy, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Choppy, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### Medium
```cs
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.Medium, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Medium, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### VibrateTriggerPulse
```cs
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.VibrateTriggerPulse, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.VibrateTriggerPulse, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### CustomTriggerValue
```cs
// With CustomTriggerValueMode
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddCustomAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.CustomTriggerValue, CustomTriggerValueMode.PulseAB, new List<int> { 0, 101, 255, 255, 0, 0, 0 });
packet = AddCustomAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.CustomTriggerValue, CustomTriggerValueMode.PulseAB, new List<int> { 0, 101, 255, 255, 0, 0, 0 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### Resistance
```cs
// Needs 2 Params in List<int> (Start: 0-9) -> (Force: 0-8)
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.Resistance, new List<int> { 0, 8 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Resistance, new List<int> { 0, 8 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### Bow
```cs
// Needs 4 Params in List<int> (Start: 0-8) -> (End: 0-8) -> (Force: 0-8) -> (SnapForce: 0-8)
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.Resistance, new List<int> { 0, 8, 2, 5 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Resistance, new List<int> { 0, 8, 2, 5 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### Galloping
```cs
// Needs 5 Params in List<int> (Start: 0-8) -> (End: 0-9) -> (FirstFoot: 0-6) -> (SecondFoot: 0-7) -> (Frequency: 0-255)
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.Galloping, new List<int> { 0, 9, 2, 4, 10 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Galloping, new List<int> { 0, 9, 2, 4, 10 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### SemiAutomaticGun
```cs
// Needs 3 Params in List<int> (Start: 2-7) -> (End: 0-8) -> (Force: 0-8)
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.SemiAutomaticGun, new List<int> { 2, 7, 8 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.SemiAutomaticGun, new List<int> { 2, 7, 8 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### AutomaticGun
```cs
// Needs 3 Params in List<int> (Start: 2-7) -> (End: 0-8) -> (Force: 0-8)
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.AutomaticGun, new List<int> { 0, 8, 10 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.AutomaticGun, new List<int> { 0, 8, 10 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### Machine
```cs
// Needs 6 Params in List<int> (Start: 0-8) -> (End: 0-9) -> (StrengthA: 0-7) -> (StrengthB: 0-7) -> (Frequency: 0-255) -> (Period: 0-2)
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.Machine, new List<int> { 0, 9, 7, 7, 10, 0 });
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.Machine, new List<int> { 0, 9, 7, 7, 10, 0 });

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________

#### VIBRATE_TRIGGER_10Hz
```cs
// Applies Vibration Effect with 10 Hz (Frequency)
// Usage ==============
// (LEGACY // Avoid Using)

Packet packet = new Packet();
int controllerIndex = 0;

packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Left, TriggerMode.VIBRATE_TRIGGER_10Hz, new List<int>());
packet = AddAdaptiveTriggerToPacket(packet, controllerIndex, Trigger.Right, TriggerMode.VIBRATE_TRIGGER_10Hz, new List<int>());

SendDataToDSX(packet);
GetDataFromDSX();
```
___________________
