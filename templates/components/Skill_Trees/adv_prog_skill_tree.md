## Skill Tree Part 1

<!-- .slide: data-auto-animate -->
:::{class="mermaid"}
```{=html}
graph LR

<div class="fragment">
A[AP Computer Science] --> B[Introduction to Programming]
A --> C[Algorithms and Problem Solving]
A --> D[Data Structures]
A --> E[Object-Oriented Programming]
A --> F[Software Development]
</div>

<div class="fragment">
C --> G[Control Structures]
C --> H[Iteration]
C --> I[Recursion]

D --> J[Arrays]
D --> K[Linked Lists]
D --> L[Stacks]
D --> M[Queues]
D --> N[Trees]
D --> O[Graphs]

E --> P[Classes and Objects]
E --> Q[Inheritance]
E --> R[Polymorphism]
E --> S[Abstract Classes and Interfaces]

F --> T[Testing and Debugging]
F --> U[Documentation]
F --> V[Version Control]
F --> W[Software Development Life Cycle]

J --> K
J --> L
K --> N
N --> O
O --> N

P --> Q
Q --> R
R --> S

T --> U
U --> V
V --> W
</div>
```
:::