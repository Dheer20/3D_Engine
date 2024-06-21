import math as m

# Defining Functions and Objects
class Vector():
    def __init__(self,x=0,y=0,z=0,w=1) -> None:
        self.x = float(x)
        self.y = float(y) 
        self.z = float(z)
        self.w = float(w)

    def Normalize(self):
        len = (self.x**2 + self.y**2 + self.z**2) ** 0.5
        if len != 0:
            self.x /= len
            self.y /= len
            self.z /= len
    
    def Make3D(self):
        if self.w != 0:    
            self.x /= self.w
            self.y /= self.w
            self.z /= self.w
            self.w /= self.w
        else: print('W is 0')

    def __matmul__(self,other:'Vector')-> 'Vector': #CROSS PRODUCT
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x)
    
    def __mul__(self,other: float)-> 'Vector':
        return Vector(self.x * other ,self.y * other ,self.z * other)

    def __pow__(self,other:'Vector')-> float: #DOT PRODUCT
        return self.x*other.x+self.y*other.y+self.z*other.z
    
    def __str__(self):
        self.Make3D
        return f"({self.x},{self.y},{self.z})"

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y}, z={self.z}, w={self.w})"
 
class Triangle():
    def __init__(self, v0=(1,1,1), v1=(2,2,2), v2=(3,3,3) ,color=None ,order=None)  -> None:
        self.v0 = Vector(*v0)
        self.v1 = Vector(*v1)
        self.v2 = Vector(*v2)
        self.color = color
        self.order = order
    
    def GetColor(self,intensity) -> None:
        color_value = int(intensity * 255)
        self.color = (color_value,color_value ,color_value)

class Matrix_3D():
    def __init__(self,matrix=[[0,0,0,0] for _ in range(4)]) -> None:
        self.matrix = matrix
    
    def __add__(self,other: 'Matrix_3D')-> 'Matrix_3D':
        return Matrix_3D(
            [a+b for a,b in zip(row1,row2)] 
            for row1,row2 in zip(self.matrix,other.matrix))

    __radd__ = __add__
    
    def __sub__(self,other :'Matrix_3D')-> 'Matrix_3D':
        return Matrix_3D(
            [a-b for a,b in zip(row1,row2)] 
            for row1,row2 in zip(self.matrix,other.matrix))
    
    __rsub__ = __sub__
    
    def __mul__(self,other: float)-> 'Matrix_3D':
        return Matrix_3D([a*other for a in row] for row in self.matrix)

    def __matmul__(self,other:'Matrix_3D')-> 'Matrix_3D':
        result = Matrix_3D()
        for i in range(4):
            for j in range(4):
                temp=0
                for k in range(4):
                    temp += self.matrix[i][k] * other.matrix[k][j]
                result.matrix[i][j] = temp
        return result
        
    def __str__(self):
        return '\n'.join(' '.join(map(str,row)) for row in self.matrix)
    
    @classmethod
    def Identity(self):
        return self([[1,0,0,0],
                     [0,1,0,0],
                     [0,0,1,0],
                     [0,0,0,1]])

    @classmethod
    def Projection(self,A,FOV,Zn,Zf)->list:
        T = Zf/(Zf-Zn)
        P = 1/m.tan(m.radians(FOV)/2)
        return self ([[P/A,0,0,0]
                     ,[0,P,0,0]
                     ,[0,0,T,-Zf*T]
                     ,[0,0,1,0]])

    
    @classmethod
    def X_Rotation(self,Angle):
        return self([[1,0,0,0]
                    ,[0,m.cos(Angle),-m.sin(Angle),0]
                    ,[0,m.sin(Angle),m.cos(Angle),0]
                    ,[0,0,0,1]])

        
    @classmethod
    def Y_Rotation(self,Angle):
        return self([[m.cos(Angle),0,m.sin(Angle),0]
                    ,[0,1,0,0]
                    ,[-m.sin(Angle),0,m.cos(Angle),0]
                    ,[0,0,0,1]])


    @classmethod
    def Z_Rotation(self,Angle):
        return self([[m.cos(Angle),-m.sin(Angle),0,0]
                    ,[m.sin(Angle),m.cos(Angle),0,0]
                    ,[0,0,1,0]
                    ,[0,0,0,1]])
    
    @staticmethod
    def MatVectorMul(i,m) -> Vector:# i is input vector , m is 4x4 matrix to be multiplied
        m = m.matrix
        result = Vector()
        result.x = i.x * m[0][0] + i.y * m[0][1] + i.z * m[0][2] + m[0][3]
        result.y = i.x * m[1][0] + i.y * m[1][1] + i.z * m[1][2] + m[1][3]
        result.z = i.x * m[2][0] + i.y * m[2][1] + i.z * m[2][2] + m[2][3]
        result.w = float(i.x * m[3][0] + i.y * m[3][1] + i.z * m[3][2] + m[3][3])
        Vector.Make3D(result)
        return result
    
    @staticmethod
    def MatTriMul(t,m)-> Triangle:
        result = Triangle()
        result.v0 = Matrix_3D.MatVectorMul(t.v0,m)
        result.v1 = Matrix_3D.MatVectorMul(t.v1,m)
        result.v2 = Matrix_3D.MatVectorMul(t.v2,m)
        return result
        

class Mesh_3D():
    def __init__(self,triangles) -> None:
        self.triangles = triangles

    def LoadObjFile(filename):
        vertices = []
        triangles = []

        with open(filename, 'r') as file:
            for line in file:
                # Ignore comments and empty lines
                if line.startswith('#') or line.strip() == '':
                    continue

                # Parse vertex lines
                if line.startswith('v '):
                    parts = line.split()
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    vertex = (x, y, z)  # Store vertices as iterable objects
                    vertices.append(vertex)

                # Parse face lines
                elif line.startswith('f '):
                    parts = line.split()
                    vertex_indices = [int(part.split('/')[0]) - 1 for part in parts[1:4]]  # -1 to convert to zero-based index
                    v0, v1, v2 = vertices[vertex_indices[0]], vertices[vertex_indices[1]], vertices[vertex_indices[2]]
                    triangle = Triangle(v0, v1, v2)
                    triangles.append(triangle)

        return Mesh_3D(triangles)
    
if __name__ == '__main__':
    A = Matrix_3D.Identity()
    B = Matrix_3D.Identity()
    C = B*10 - A
    print(C)