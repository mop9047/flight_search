## How to Start?

1. Go to terminal and run this code `git clone https://github.com/mop9047/flight_search.git`
2. Run `pip install flask` and `pip install mysql`

## Run in Your Computer

1. Start the database in MAMP
2. Create a databse called 'blog' and enter the queries from `simple.sql` to have the tables setup
3. Run the `run.py` in vscode and paste the url `http://127.0.0.1:8889` in your browser

## Make a new branch

The main branch is where the final approved code will be. For testing, make a branch first to keep you own changes trackable.

1. Go to the terminal assigned to the cloned repository and run `git checkout -b your_branch` where **your branch** is the name of the branch, best to put your name and the feature you are working on (E.g John_Add_Flights).
2. Commit your changes
3. Check with `git branch` to see branch. The one with the \* is the current branch you are working on.

## Pull Request

1. When done with the code, do a pull request to merge your changes with the main branch
