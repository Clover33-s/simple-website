import hashlib
import time
import multiprocessing
import os

class MulticoreMiner:
    def __init__(self):
        pass

    @staticmethod
    def _mine_worker(worker_id, block_data, difficulty, start_nonce, end_nonce, result_queue):
        """Worker function to be run in a separate process."""
        target = "0" * difficulty
        nonce = start_nonce

        # Optimization: Localize hashlib.sha256 for slight speedup in tight loop
        sha256 = hashlib.sha256

        while nonce < end_nonce:
            # Check if another worker found the solution (optional, but queue check is expensive)
            # Just mine until range exhausted or external termination

            text = f"{block_data}{nonce}".encode()
            hash_result = sha256(text).hexdigest()

            if hash_result.startswith(target):
                result_queue.put((nonce, hash_result, worker_id))
                return

            nonce += 1

        # Determine if we should signal completion or just exit
        return

    def mine(self, block_data, difficulty, num_threads=None):
        """
        Starts the mining process using multiprocessing.
        Returns: (nonce, hash, time_taken, hashrate)
        """
        if num_threads is None:
            num_threads = multiprocessing.cpu_count()

        # Define a large search space
        max_nonce = 100000000 # Adjust based on expected difficulty or make infinite
        chunk_size = max_nonce // num_threads

        manager = multiprocessing.Manager()
        result_queue = manager.Queue()
        processes = []

        start_time = time.time()

        for i in range(num_threads):
            start = i * chunk_size
            end = start + chunk_size
            p = multiprocessing.Process(
                target=self._mine_worker,
                args=(i, block_data, difficulty, start, end, result_queue)
            )
            processes.append(p)
            p.start()

        # Wait for result
        found_nonce = None
        found_hash = None

        # We poll the queue or wait for processes
        while True:
            # Check if any result found
            if not result_queue.empty():
                found_nonce, found_hash, worker_id = result_queue.get()
                # Terminate all
                for p in processes:
                    p.terminate()
                break

            # Check if all processes finished (failed to find in range)
            if all(not p.is_alive() for p in processes):
                break

            time.sleep(0.1)

        end_time = time.time()
        duration = end_time - start_time

        # Approximate hashrate (If found, we don't know exact count of all threads,
        # but we can estimate based on nonce found or max range if not found)
        # For simplicity in this simulation:
        # If found: hashrate ~ found_nonce / duration (very rough, only counts winner thread work)
        # Better: run a benchmark mode for hashrate.
        # For 'Simulation', just returning the result is enough.

        return found_nonce, found_hash, duration
