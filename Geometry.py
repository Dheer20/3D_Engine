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

    def Tuple(self):
        return (self.x,self.y,self.z)

    @classmethod
    def TwoPoint(self,point1,point2):
        return Vector(point1.x - point2.x,point1.y - point2.y,point1.z - point2.z)
    
    def __add__(self,other : 'Vector')-> 'Vector':
        return Vector(
            self.x+other.x,
            self.y+other.y,
            self.z+other.z,)
    
    __radd__ = __add__
    
    def __sub__(self,other : 'Vector')-> 'Vector':
        return Vector(
            self.x-other.x,
            self.y-other.y,
            self.z-other.z,)
    
    __rsub__ = __sub__

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
    
    def GetColor(self,shadow : tuple[int] ,highlight : tuple[int],intensity : float) -> None:
        self.color = tuple(round(a+(b-a)*intensity,3) for a,b in zip(shadow,highlight))

    def __repr__(self):
        return f"v0 = {self.v0}, v1 = {self.v1}, v2 = {self.v2}"

class Matrix_3D():
    def __init__(self,matrix=None) -> None:
        self.matrix = list(matrix) if matrix else [[0,0,0,0] for _ in range(4)]
    
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
    
    __rmatmul__ = __matmul__
        
    def __str__(self):
        return '\n'.join(' '.join(map(str,row)) for row in self.matrix)
    
    @classmethod
    def Identity(self):
        return self([[1,0,0,0],
                     [0,1,0,0],
                     [0,0,1,0],
                     [0,0,0,1]])

    @classmethod
    def Projection(self,A,FOV,Zn,Zf):
        T = Zf/(Zf-Zn)
        P = 1/m.tan(m.radians(FOV)/2)
        return self ([[P/A,0,0,0]
                     ,[0,P,0,0]
                     ,[0,0,T,-Zn*T]
                     ,[0,0,1,0]])

    @classmethod
    def View_for_CameraPointAt(self,cam_position : Vector,target : Vector,up_vector : Vector):
        # Calculating new forward vector
        new_forward : Vector = target-cam_position
        new_forward.Normalize()
        
        # Calculating new up vector
        new_up : Vector = up_vector - (new_forward * (up_vector ** new_forward))
        new_up.Normalize()

        #Calculating New right vector
        new_right : Vector = new_up @ new_forward
        new_right.Normalize()

        return self([[new_right.x,new_right.y,new_right.z,-(cam_position**new_right)],
                     [new_up.x,new_up.y,new_up.z,-(cam_position**new_up)],
                     [new_forward.x,new_forward.y,new_forward.z,-(cam_position**new_forward)],
                     [0,0,0,1]]),new_right
    
    @classmethod
    def Translation(self,X = 0,Y = 0,Z =0):
        return self([[1,0,0,X],
                     [0,1,0,Y],
                     [0,0,1,Z],
                     [0,0,0,1]])
    
    @classmethod
    def Scale(self,X = 1,Y = 1,Z = 1):
        return self([[X,0,0,0],
                     [0,Y,0,0],
                     [0,0,Z,0],
                     [0,0,0,1]])

    @classmethod
    def X_Rotation(self,Angle):
        return self([[1,0,0,0]
                    ,[0,m.cos(Angle),-m.sin(Angle),0]
                    ,[0,m.sin(Angle),m.cos(Angle),0]
                    ,[0,0,0,1]])

        
    @classmethod
    def Y_Rotation(self,Angle):
        return self([[m.cos(Angle),0,-m.sin(Angle),0]
                    ,[0,1,0,0]
                    ,[m.sin(Angle),0,m.cos(Angle),0]
                    ,[0,0,0,1]])


    @classmethod
    def Z_Rotation(self,Angle):
        return self([[m.cos(Angle),-m.sin(Angle),0,0]
                    ,[m.sin(Angle),m.cos(Angle),0,0]
                    ,[0,0,1,0]
                    ,[0,0,0,1]])
    
    @staticmethod
    def MatVectorMul(i : Vector,m: 'Matrix_3D') -> Vector:
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

class Plane():
    def __init__(self,normal : Vector,point : Vector):
        self.normal = normal
        self.point = point
        normal.Normalize()
        self.distance = - normal**point
    
    def classify_point(self,point : Vector):
        return (self.normal**point) + self.distance
    
    def interpolate_point(self,t : float,start : Vector,end : Vector):
        return start + (end - start)*t
    
    def clip_triangle(self,triangle : Triangle)-> list[Triangle]:
        vertices       =   [(i,vertex) for i,vertex in enumerate([triangle.v0,triangle.v1,triangle.v2])]
        inside_points  =   [(i,vertex) for i,vertex in vertices if self.classify_point(vertex) >= 0]
        outside_points =   [(i,vertex) for i,vertex in vertices if self.classify_point(vertex) < 0]

        count_inside = len(inside_points)

        if count_inside == 0:
            return []
        elif count_inside == 3:
            return [triangle]
        
        elif count_inside == 1:
            (in_index,v_in) = inside_points[0]
            (out_index1 , v_out1),(out_index2 , v_out2)= outside_points

            t1 = self.classify_point(v_in)/(self.classify_point(v_in)-self.classify_point(v_out1))
            t2 = self.classify_point(v_in)/(self.classify_point(v_in)-self.classify_point(v_out2))

            new_v1 = self.interpolate_point(t1,v_in,v_out1)
            new_v2 = self.interpolate_point(t2,v_in,v_out2)

            new_vertices = [None,None,None]
            new_vertices[in_index]   =   v_in.Tuple()
            new_vertices[out_index1] = new_v1.Tuple()
            new_vertices[out_index2] = new_v2.Tuple()

            return [Triangle(*new_vertices,color = triangle.color)]
        elif count_inside == 2:
            (in_index1,v_in1),(in_index2,v_in2) = inside_points
            (out_index,v_out) = outside_points[0]

            t1 = self.classify_point(v_in1)/(self.classify_point(v_in1)-self.classify_point(v_out))
            t2 = self.classify_point(v_in2)/(self.classify_point(v_in2)-self.classify_point(v_out))

            new_v1 = self.interpolate_point(t1,v_in1,v_out)
            new_v2 = self.interpolate_point(t2,v_in2,v_out)

            new_vertices1 = [None,None,None]
            new_vertices1[in_index1] =  v_in1.Tuple()
            new_vertices1[in_index2] =  v_in2.Tuple()
            new_vertices1[out_index] = new_v1.Tuple()

            new_vertices2 = [None,None,None]
            new_vertices2[in_index1] =  v_in2.Tuple()
            new_vertices2[in_index2] = new_v1.Tuple()
            new_vertices2[out_index] = new_v2.Tuple()

            return [Triangle(*new_vertices1,color = triangle.color),Triangle(*new_vertices2,color = triangle.color)]
        else:
            print(f"Unexpected number of inside points: {count_inside}")
            return [triangle]

if __name__ == '__main__':

    print('run D_Engine not Geometry file')