# KanbanSYSTEM

  What is Kanban board ?
  
    A Kanban board is a tool for workflow visualization and one of the Kanban method's key components.
  Visualizing your workflow and tasks on a  Kanban board helps you better understand your processes 
  and gain an overview of your workload.It aims to help you visualize your work, maximize efficiency, 
  and improve continuously.
  
  ---For more information: https://kanbanize.com/kanban-resources/getting-started/what-is-kanban-board
  Project_ideas in project_ideas.txt (bulgarian)
  
  
  This web application represents a simple Kanban board with three columns: TODO, IN PROGRESS, DONE.
  It includes the following features:
     * Authentication system
         - login
         - register
         - change password
         - password recovery 
              * it is working only in a develepment envrionment(terminal mode)        
     
     * Homepage, accessible to everyone
     * System accessible only by the authenticated user.
     * User
        - full crud for his todos
                 * every user has his own personal todo_page
        - he can create his own companies (work groups)
                 * it can add/removes users to its companies (employees) and be their boss
                 * he can create todos for some of his companies only
                 * he can assign a user a todo based on which company he is "hired" by.
                 * the assigned todos can be fully CRUD-ed only by the company boss:
                 * when a todo is assigned to someone it immediately show up in their personal kanban opage.
                 * to every todo can be added notes by the Kanban master
                 
                 
                 (UPDATE REQUIRED
               
                 
  

