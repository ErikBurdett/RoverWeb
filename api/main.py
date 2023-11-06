import sys
import os

sys.path.append(os.path.dirname(__file__))
sys.dont_write_bytecode=True

from website import create_app

app = create_app()

if __name__ == '__main__':
  app.run()
  
