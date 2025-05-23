import multiprocessing
import psutil
import sys
import os


def calcurator(n):
    
    if n < 0:
        return n
    else:
        return calcurator( n - 1 ) + calcurator( n - 2 )



def cpu_stress():
    try:
        while True:
            cpu_usage = psutil.cpu_percent()
            calcurator(20)
            sys.stdout.write(f"\rCPU Process {multiprocessing.current_process().name} CPU Usage : {round(cpu_usage)} %")    
            sys.stdout.flush()
    except Exception as e:
        python = sys.executable
        script_path = os.path.abspath(sys.argv[0])
        os.execv(python,[python,script_path])
        
        print(f"ERROR {e}")
    except KeyboardInterrupt:
        print("Exit")

def main():
    
    num_processes = multiprocessing.cpu_count()
    processes = []
    
    for _ in range(num_processes):
        process = multiprocessing.Process(target=cpu_stress)
        processes.append(process)
        process.start()
        
    for process in processes:
        process.join()
    
    
    
    
    
if __name__ == '__main__':
    main()