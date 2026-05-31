# Design: Power-up Enemy Eating Mechanic

**Date:** 2026-05-31  
**Feature:** Add ability for player to eat enemies after consuming big pellet (power-up)  
**Status:** Design Approved

---

## Overview

When the player eats a big pellet (PowerPellet), they enter a **5-second "super mode"** where:
- Enemies become vulnerable
- Player can eat enemies for +100 points each
- Eaten enemies reset to spawn position and freeze for 15 seconds
- No visual changes (mechanics only)

---

## Architecture

### Player Changes (actors.py)

Add one flag to `Player` class:
```python
self.super_mode_active = False
```

This flag indicates whether super mode is currently active. No timer stored in Player.

### Game Loop Changes (main.py)

Add two module-level variables to `game_loop()`:

```python
super_mode_timer = 0  # Countdown in frames (60fps)
enemy_freeze_timers = {}  # Dict: enemy_object -> frames_remaining
```

**Timer constants (in frames @ 60fps):**
- `super_mode_timer`: 5 seconds = 300 frames
- `enemy_freeze_timers`: 15 seconds = 900 frames per enemy

### Data Flow

1. **Power-up Consumed:**
   - Collision: gracz-dużej_kulki → `super_mode_active = True`, `super_mode_timer = 300`

2. **Enemy Eaten (during super mode):**
   - Collision: gracz-wróg AND `super_mode_active == True`
   - Action:
     - `enemy.goto(spawn_x, spawn_y)` — reset position
     - `enemy_freeze_timers[enemy] = 900` — freeze for 15 sec
     - `player.score += 100`

3. **Normal Collision (no super mode):**
   - Collision: gracz-wróg AND `super_mode_active == False`
   - Action: Original behavior (−1 life, player reset)

4. **Frame Update (every frame):**
   - Decrement `super_mode_timer` by 1
   - If `super_mode_timer <= 0`: `super_mode_active = False`
   - Decrement all `enemy_freeze_timers[enemy]` by 1
   - Remove entries where timer <= 0
   - Skip movement/chasing for frozen enemies (see Freezing Logic)

---

## Implementation Details

### Freezing Logic

Before `enemy.move()` and `enemy.go_after_player()`:

```python
for enemy in enemies:
    # Skip frozen enemies
    if enemy in enemy_freeze_timers:
        continue
    
    # Normal enemy logic
    enemy.move()
    enemy.check_wall_collision()
    enemy.go_after_player()
```

This prevents frozen enemies from moving or chasing.

### Collision Detection (lines 154-165 in current game_loop)

Replace existing enemy-player collision block:

```python
if enemy.distance(player) < CELL_SIZE / 2:
    if player.super_mode_active:
        # Eating enemy
        os.system("aplay eat.wav > /dev/null 2>&1 &")
        enemy.goto(enemy_spawn_position[enemy])  # Need to track spawn positions
        enemy_freeze_timers[enemy] = 900
        player.score += 100
    else:
        # Normal collision
        os.system("aplay death.wav > /dev/null 2>&1 &")
        safe_spots = [...]  # Existing logic
        player.goto(random.choice(safe_spots))
        player.lives -= 1
```

**Note:** Need to track enemy spawn positions. Store in a dict: `enemy_spawn_positions = {enemy: (x, y)}`

### Power-up Consumption (lines 135-144)

Replace existing power-pellet collision block:

```python
for (px, py), stamp_id in list(power_pen.stamps.items()):
    if player.distance(px, py) < CELL_SIZE / 2:
        os.system("aplay eat.wav > /dev/null 2>&1 &")
        power_pen.clearstamp(stamp_id)
        del power_pen.stamps[(px, py)]
        player.score += 50
        
        # ADDED: Activate super mode
        player.super_mode_active = True
        super_mode_timer = 300  # 5 seconds @ 60fps
        
        # Existing speedup
        player.move_speed += 3
        screen.ontimer(player.reset_speed, 3000)
```

### Timer Decrement (beginning of game_loop)

Add before all collision/movement logic:

```python
# Decrement super mode timer
if super_mode_timer > 0:
    super_mode_timer -= 1
    if super_mode_timer <= 0:
        player.super_mode_active = False

# Decrement and clean up freeze timers
for enemy in list(enemy_freeze_timers.keys()):
    enemy_freeze_timers[enemy] -= 1
    if enemy_freeze_timers[enemy] <= 0:
        del enemy_freeze_timers[enemy]
```

---

## Edge Cases

### 1. Power-up eaten while super mode active
- Timer resets to 300 frames
- Effect: Extends super mode by 5 more seconds (or resets to 5 seconds total, depending on intent)
- **Decision:** Reset to 300 (extends by effectively 5 sec if currently <5 sec remaining)

### 2. Enemy eaten while frozen
- Cannot happen — frozen enemies skip movement AND collision block
- If somehow attempted: ignore, enemy stays frozen until timer expires

### 3. Level transition during super mode
- Super mode state resets naturally (new game_loop instance)
- No cleanup needed

### 4. Enemy eaten -> frozen -> level ends
- Frozen list cleared when `screen.clear()` called in `load_next_level()`
- No issue

### 5. Player collision with wall while in super mode
- Unaffected — wall collision logic unchanged

---

## Testing Strategy

### Manual Testing
1. Eat big pellet → verify super_mode_active = True for 5 seconds
2. Collide with enemy during super mode → enemy resets, freezes, +100 points
3. Collide with enemy after super mode ends → normal death/respawn
4. Eat multiple enemies in one super mode → verify all freeze independently
5. Frozen enemy unfreezes after 15 seconds → resumes normal AI

### Edge Cases
- Eat power-up while super mode active → timer resets
- Multiple enemies frozen simultaneously → all unfreeze on schedule
- Level transition during freeze → clean state on reload

---

## Files Modified

- `actors.py` — Add `super_mode_active` flag to Player
- `main.py` — Add timers, collision logic, freeze skipping, enemy spawn tracking

## No Changes Required
- `constants.py` — Use existing frame timing (1000 // 60)
- `renderer.py` — No visual changes
- `mazes.py` — No changes

---

## Success Criteria

✓ Player can eat enemies for 5 seconds after consuming power-up  
✓ Eaten enemies: +100 points, reset position, freeze 15 seconds  
✓ Frozen enemies don't move or chase  
✓ Super mode ends after 5 seconds (or resets if power-up eaten again)  
✓ Normal game mechanic unaffected outside super mode  
✓ All edge cases handled gracefully
