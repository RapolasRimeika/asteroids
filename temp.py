                    state.player.score_points(1)
                    state.player.destroy_asteroid(1)



        # Check for collisions between shots and asteroids
        for shot in shots:
            for asteroid in asteroid_group:
                if shot.collision(asteroid, bounce=False):
                    asteroid.split()
                    state.player.score_points(1)
                    state.player.destroy_asteroid(1)
                    shot.kill()
                    break  # Move to the next shot