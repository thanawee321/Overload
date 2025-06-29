import psutil
import gc
import time
import sys
import os 
import random
import argparse

def restart():
    
    python = sys.executable
    script_path = os.path.abspath(sys.argv[0])
    os.execv(python,[python,script_path])
    
    return True


def main(args):
    
    target_usage = args.target
    stack = args.percent / 100
    
    ram_system = psutil.virtual_memory().total
    chunk_size = ram_system * stack
    
    array_block = []
    
    try:
        
        start_time = time.strftime("%H:%M:%S")
        start_usage = time.time()
        end_usage = None
        
        while True:
            current_ram_usage = psutil.virtual_memory().percent
            current_memory_usage = psutil.Process().memory_info().rss / (1024 * 1024)
            current_time = time.strftime("%H:%M:%S")
            
            if current_ram_usage < target_usage:
                block = bytearray(int(chunk_size))
                for i in range(0,len(array_block),4096):
                    block[i] = random.randrange(1,255)
                array_block.append(block)
                sys.stdout.write('\r' + " " * 100 + '\r')
                sys.stdout.write('\r' + f"[{current_time}] | Percent(Target = {target_usage}%) Usage: {round(current_ram_usage)}% | RAM Usage: {current_memory_usage:.2f}MB | Insert({round( stack * 100)}%) stack {chunk_size / (1024 * 1024 ):.3f} MB ")
                sys.stdout.flush()
                
                
            if current_ram_usage > target_usage:
                if array_block:
                    
                    for _ in range(min(10,len(array_block))):
                        array_block.pop()
                        
                    gc.collect()
                    
            if current_ram_usage == target_usage:
                for i in range(60,0,-1):
                    sys.stdout.write('\r' + " " * 100 + '\r')
                    sys.stdout.write(f"\rTarget reached. Waiting...({i})")
                    sys.stdout.flush()
                array_block.clear()
                gc.collect()
                
            gc.collect()
            time.sleep(0.05)
            
            
            
    except MemoryError:
        gc.collect()
        array_block.clear()
        
        end_time = time.strftime("%H:%M:%S")
        end_usage = time.time()
        print(f"\n[{end_time}]Memory Error")
        restart()
        
    except KeyboardInterrupt:
        gc.collect()
        array_block.clear()
        
        end_time = time.strftime("%H:%M:%S")
        end_usage = time.time()
        print("\nExit")
        
    finally:
        gc.collect()
        array_block.clear()
        print(f"Memory Usage : {current_memory_usage:.2f}MB")
        
        if end_usage is not None or end_usage != None:
            elapsed_time = end_usage - start_usage
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            
            print(f"Start Time: {start_time} ---> End Time: {end_time} = {hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            print(f"Start Time: {start_time} ---> End Time: Running...")
        
        os.system('pause')
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', type=int, default=90, help="Target RAM Usage of this program (%%)")
    parser.add_argument('-p', '--percent', type=int, default=1, help="Memory to insert per stack (%%)")
    args = parser.parse_args()
    main(args)
                    