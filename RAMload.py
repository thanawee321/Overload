import psutil
import gc
import time
import sys
import os



def restart():
    
    python = sys.executable
    script_path = os.path.abspath(sys.argv[0])
    os.execv(python,[python,script_path])


def main():
    
    ram_system = psutil.virtual_memory().total
    target_usage = 89
    chunk_size = ram_system * 0.01
    
    array_block = []
    
    try:
        start_time = time.strftime("%H:%M:%S")
        start_usage = time.time()
        end_usage = None
        while True:
            current_ramUsage = psutil.virtual_memory().percent
            current_time = time.strftime("%H:%M:%S")
            current_memory = psutil.Process().memory_info().rss / (1024 * 1024)
        
            if current_ramUsage < target_usage:
                array_block.append(bytearray(int(chunk_size)))
                sys.stdout.write('\r' + ' ' * 80 + '\r')
                sys.stdout.write(f"\r [{current_time}] | Percent Usage: {round(current_ramUsage)}% | RAM Usage: {current_memory:.2f}MB | Insert stack {chunk_size / (1024 * 1024 ):.3f} MB")
                sys.stdout.flush()
                
            if current_ramUsage == target_usage:
                for i in range(30,-1,-1):
                    sys.stdout.write('\r' + ' ' * 80 + '\r')
                    sys.stdout.write(f"Hole ram usage at {current_ramUsage}% ({i})")
                    sys.stdout.flush()
                    time.sleep(1)
                array_block.clear()
                
            if current_ramUsage > target_usage:
                if array_block:
                    for _ in range(min(10,len(array_block))):
                        array_block.pop()
                    gc.collect()
                    
                    
            gc.collect()
            time.sleep(0.05)
    except MemoryError:
        gc.collect()
        array_block.clear()
        end_time = time.strftime("%H:%M:%S")
        end_usage = time.time()
        print(f"\nMemory ERROR")
        restart()
        
    except KeyboardInterrupt:
        gc.collect()
        array_block.clear()
        end_time = time.strftime("%H:%M:%S")
        end_usage = time.time()
        print(f"\nExit")


    finally:
        gc.collect()
        array_block.clear()
        
        if end_usage is not None:
            elapsed_time = end_usage - start_usage
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            
            print(f"Start Time: {start_time} -> End Time: {end_time} = {hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            print(f"Start Time: {start_time} -> End Time: Running...") 
        
        input("Please Enter ... ")
        
if __name__ == '__main__':
    main()
        