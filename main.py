from front_end import App
from database import criar_banco
 
if __name__ == "__main__":
 
    criar_banco()
 
    app = App()
    app.mainloop()
   
#fim do Codigo