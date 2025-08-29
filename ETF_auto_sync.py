import os
import subprocess
import time
from datetime import datetime

def main():
    print("=" * 50)
    print("    ETF FEED AUTO SYNC - PYTHON VERSION")
    print("=" * 50)
    print()
    
    # Change to ETF-Feed directory
    repo_path = r"C:\Users\timot\OneDrive\Documents\GitHub\ETF-Feed"
    
    try:
        os.chdir(repo_path)
        print(f"Monitoring folder: {os.getcwd()}")
        print("Checking every 15 seconds...")
        print("Press Ctrl+C to stop")
        print()
    except:
        print(f"ERROR: Cannot access {repo_path}")
        print("Make sure the folder exists and is a Git repository")
        input("Press Enter to exit...")
        return
    
    while True:
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Checking for changes...")
            
            # Add all files first (including any new changes)
            subprocess.run(["git", "add", "."], capture_output=True)
            
            # Check if there are staged changes
            status_result = subprocess.run(["git", "status", "--porcelain"], 
                                         capture_output=True, text=True)
            staged_result = subprocess.run(["git", "diff", "--staged", "--name-only"], 
                                         capture_output=True, text=True)
            
            if staged_result.stdout.strip():  # There are staged changes ready to commit
                staged_files = staged_result.stdout.strip().split('\n')
                print(f"  Changes detected in {len(staged_files)} files")
                print("  Files:", ', '.join(staged_files[:5]) + ('...' if len(staged_files) > 5 else ''))
                
                # Commit changes
                commit_msg = f"Auto-update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                commit_result = subprocess.run(["git", "commit", "-m", commit_msg], 
                                             capture_output=True, text=True)
                
                if commit_result.returncode == 0:
                    print("  ✓ Committed successfully")
                    
                    # Push to GitHub
                    print("  → Pushing to GitHub...")
                    push_result = subprocess.run(["git", "push", "origin", "main"], 
                                               capture_output=True, text=True)
                    
                    if push_result.returncode == 0:
                        print("  ✓ Successfully pushed to GitHub!")
                        print("  ✓ Files are live online!")
                    else:
                        print("  ✗ Push failed:")
                        if push_result.stderr:
                            print(f"    {push_result.stderr.strip()}")
                else:
                    print("  ✗ Commit failed:")
                    if commit_result.stderr:
                        print(f"    {commit_result.stderr.strip()}")
            else:
                print("  No changes found")
            
            print()
            time.sleep(15)  # Wait 15 seconds
            
        except KeyboardInterrupt:
            print("\n\nStopping auto-sync...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(15)

if __name__ == "__main__":
    main()