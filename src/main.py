# main.py - Astartes-Gotchi Main Entry Point
# This is the game loop - runs after boot.py

import gc
import time
from lib.space_marine import SpaceMarine
from lib.ui import AstartesUI
from lib.save_manager import SaveManager
import config

def main():
    """Main game loop"""
    print("\n" + "=" * 40)
    print("FOR THE EMPEROR! 🦅")
    print("ASTARTES-GOTCHI v0.1.0 - MVP")
    print("=" * 40 + "\n")

    # Initialize UI (hardware)
    print(">>> Initializing display and input...")
    ui = AstartesUI()
    ui.show_boot_screen()

    # Load or create marine
    print(">>> Loading Space Marine data...")
    save_mgr = SaveManager()
    marine_data = save_mgr.load()

    if marine_data:
        print(f">>> Restoring Battle Brother: {marine_data.get('name', 'Unknown')}")
        marine = SpaceMarine.from_dict(marine_data)
    else:
        print(">>> No save found - creating new Neophyte")
        marine = SpaceMarine(name=config.DEFAULT_MARINE_NAME)
        save_mgr.save(marine.to_dict())

    print(f">>> Marine status: Stage {marine.current_stage}, Age {marine.age_cycles} cycles")
    print(f">>> Corruption: {marine.corruption}%, Discipline: {marine.discipline}%")

    # Main game loop
    print(">>> Entering main game loop...\n")

    last_update = time.time()
    last_save = time.time()
    frame_count = 0

    try:
        while marine.is_alive:
            # Frame timing
            frame_start = time.time()

            # Update marine stats (passive decay)
            current_time = time.time()
            if current_time - last_update >= config.UPDATE_INTERVAL:
                marine.update()
                last_update = current_time

            # Handle input (touch buttons)
            action = ui.get_input()
            if action:
                handle_action(action, marine, ui)

            # Render screen
            ui.render(marine)

            # Auto-save every 30 seconds
            if current_time - last_save >= config.AUTOSAVE_INTERVAL:
                save_mgr.save(marine.to_dict())
                last_save = current_time
                print(f">>> [Autosave] Cycle {marine.age_cycles}")

            # Check evolution conditions
            if marine.should_evolve():
                ui.show_evolution_cutscene(marine)
                marine.evolve()
                save_mgr.save(marine.to_dict())

            # Frame rate limiting (10 FPS target)
            frame_duration = time.time() - frame_start
            sleep_time = max(0, config.FRAME_TIME - frame_duration)
            time.sleep(sleep_time)

            frame_count += 1

            # Periodic garbage collection
            if frame_count % 100 == 0:
                gc.collect()

    except KeyboardInterrupt:
        print("\n>>> User interrupt detected")

    except Exception as e:
        print(f"\n>>> FATAL ERROR: {e}")
        import sys
        sys.print_exception(e)
        ui.show_error_screen(str(e))

    finally:
        # Final save before exit
        print("\n>>> Saving final state...")
        save_mgr.save(marine.to_dict())

        # Show death screen if marine died
        if not marine.is_alive:
            print(f">>> Marine has fallen: {marine.death_cause}")
            ui.show_death_sequence(marine)

        print("\n>>> Game session ended")
        print("FOR THE EMPEROR! 🦅\n")


def handle_action(action, marine, ui):
    """Handle player input actions"""
    print(f">>> Action: {action}")

    if action == "feed":
        ui.show_feed_menu(marine)
    elif action == "combat":
        ui.show_combat_menu(marine)
    elif action == "pray":
        marine.pray()
    elif action == "clean":
        marine.clean()
    elif action == "status":
        ui.show_status_screen(marine)
    elif action == "power":
        # Save before power off
        from lib.save_manager import SaveManager
        save_mgr = SaveManager()
        save_mgr.save(marine.to_dict())
        print(">>> Saved before power off")
        ui.power_off()
    else:
        print(f">>> Unknown action: {action}")


if __name__ == "__main__":
    main()
