"""
WRITE A CLASS DOCUMENTATION
"""

class Frame:
    
    dr = 0.05

    def __init__(self,N_,phi_,x_,y_,d_,color_,L_=10.0): #,P_=[],k_=[]):
        try:
            self.N_     = N_
            self.phi_   = phi_
            self.x_     = x_
            self.y_     = y_
            self.d_     = d_
            self.color_ = color_
            self.L_     = L_
            self.P_     = []
            self.k_     = []
            self.rgb_   = []
           

            self._set_rgb()

            if len(self.x_) > self.N_:
                import warnings
                warnings.warn("len(x_) > N_", RuntimeWarning)
                self.x_ = self.x_[:self.N_]
                self.y_ = self.y_[:self.N_]
            elif len(self.x_) < self.N_:
                raise ValueError("len(self.x_) < self.N_")

        except ValueError as err:
            import sys
            print(err.args)
            print("Behavior not implemented yet. Terminating ...")
            sys.exit(1)
 

    def _set_rgb(self):
        if len(self.rgb_) > 0:
            pass
        else:
            for i in range(self.N_):
                if self.color_[i] == 1:
                    self.rgb_.append([0.7578125,0.6953125,0.5000000])
                elif self.color_[i] == 0:
                    self.rgb_.append([0.8200000,0.8200000,0.8200000])
                elif self.color_[i] == 2:
                    self.rgb_.append([1.0000000,0.0000000,0.0000000])
                else:
                    self.rgb_.append([0.0000000,1.0000000,0.0000000])


    def get_N(self):
        return self.N_

    def get_D(self,i=None):
        if i == None:
            return [dval/self.L_ for dval in self.d_]
        else:
            return self.d_[i] / self.L_
    
    def get_X(self,i=None):
        if i == None:
            return [xval/self.L_ for xval in self.x_]
        else:
            return self.x_[i] / self.L_
    
    def get_Y(self,i=None):
        if i == None:
            return [yval/self.L_ for yval in self.y_]
        else:
            return self.y_[i] / self.L_

    def get_RGB(self,i=None):
        if i == None:
            return self.rgb_
        else:
            return self.rgb_[i]
    
    def __str__(self):
        out_str  = ""
        out_str += str( self.N_ ) + " "
        out_str += str( self.phi_ ) + " "
        out_str += str( len( self.x_ ) ) + " "

        return out_str

    def calc_contacts_bonds(self):
         contacts = []
         bonds = []
         for i in range(self.N_):
             xi = self.get_X(i)
             yi = self.get_Y(i)
             di = self.get_D(i)
             for j in range(self.N_):
                 xj = self.get_X(j)
                 yj = self.get_Y(j)
                 dj = self.get_D(j)
                 if j-i == 1 and i%2 == 0:
                     bonds.append([xi,yi,xj,yj])
     
                 elif j > i:
                     dx = xi-xj 
                     dy = yi-yj 
                     dij = di+dj
                     rij2 = dx*dx + dy*dy
                     if rij2 < dij*dij:
                          contacts.append( [xi,yi,xj,yj] )
         
         return contacts,bonds



