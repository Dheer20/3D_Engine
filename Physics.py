from Geometry import Mesh_3D,Matrix_3D,Vector,Triangle

GRAVITY = -9.81
BOUNCE = 0.4
SLEEP_VEL = 0.05
LATERAL_FRICTION = 0.85

class SceneObject():
    def __init__(self,mesh: Mesh_3D,position: Vector,scale: Vector,velocity: Vector,on_ground: bool=False):
        self.mesh = mesh 
        self.position = position
        self.scale = scale
        self.velocity = velocity
        self.on_ground = on_ground
        self._get_half_height()

    def _get_half_height(self):    
        all_y=[]
        for tri in self.mesh.triangles:
            for v in (tri.v0,tri.v1,tri.v2):
                all_y.append(v.y)
        
        local_height = max(all_y) - min(all_y)
        self.half_height = (local_height / 2) * self.scale.y
    
    def _build_world_matrix(self):
        scale_mat = Matrix_3D.Scale(self.scale.x,self.scale.y,self.scale.z)
        trans_mat = Matrix_3D.Translation(self.position.x,self.position.y,self.position.z)
        return trans_mat @ scale_mat

    def world_triangles(self):
        word_mat =  self._build_world_matrix()
        for tri in self.mesh.triangles:
            wt = Matrix_3D.MatTriMul(tri,word_mat)
            wt.color = tri.color
            yield wt    

class PhysicsWorld():
    def __init__(self,gravity=None,bounce=None,sleep_vel=None,lateral_friction=None):
        self.objects = []  
        self.gravity = gravity if gravity is not None else GRAVITY
        self.bounce = bounce if bounce is not None else BOUNCE
        self.sleep_vel = sleep_vel if sleep_vel is not None else SLEEP_VEL
        self.lateral_friction = lateral_friction if lateral_friction is not None else LATERAL_FRICTION
    
    def add_object(self,obj: SceneObject):
        self.objects.append(obj)

    def add_objects(self,objs):
        self.objects.extend(objs)

    def step(self,dt):
        for obj in self.objects:
            
            if not obj.on_ground:
                # Applying gravity to vertical velocity
                obj.velocity.y += self.gravity * dt

            # Integrate position from Velocity 
            obj.position += obj.velocity * dt

            if obj.position.y <= obj.half_height:   

                obj.position.y = obj.half_height

                if abs(obj.velocity.y) < self.sleep_vel:
                    obj.velocity.y = 0
                    obj.on_ground = True
                else:
                    obj.velocity.y = -obj.velocity.y * self.bounce
                    obj.on_ground = False
                                
            else:
                obj.on_ground = False
            
            if obj.on_ground:
                obj.velocity.z *= self.lateral_friction
                obj.velocity.x *= self.lateral_friction


               