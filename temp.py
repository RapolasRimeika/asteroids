                    state.player.score_points(1)
                    state.player.destroy_asteroid(1)



        # Check for collisions between shots and asteroids
shot.collision(asteroid, bounce=False):
                    asteroid.split()
                    state.player.score_points(1)
                    state.player.destroy_asteroid(1)
                    shot.kill()
                    break  # Move to the next shot