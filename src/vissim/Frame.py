"""
WRITE A CLASS DOCUMENTATION
"""

from utils import add_image

class Frame:
    
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
         bondimages = []
         images = []
         for i in range(self.N_):
             xi = self.get_X(i)
             yi = self.get_Y(i)
             di = self.get_D(i)
             fi, li = add_image(xi, yi, 2*di)
             if fi != 0:
                 if i%2==0: # GET DAUGHTER LOBE
                     xi2 = self.get_X(i+1)
                     yi2 = self.get_Y(i+1)
                     di2 = self.get_D(i+1)
                     rgb2= self.get_RGB(i+1) 
                 else : # GET MOTHER LOBE
                     xi2 = self.get_X(i-1)
                     yi2 = self.get_Y(i-1)
                     di2 = self.get_D(i-1)

                 
                 if fi == 1: 
                     el0 = li[0]
                     el1 = li[1]
                     el2 = li[2]
                     images.append( [el0[0], el0[1], di ] )
                     images.append( [xi2+(el0[0]-xi), yi2+(el0[1]-yi), di2] )

                     images.append( [el1[0], el1[1], di ] )
                     images.append( [xi2+(el1[0]-xi), yi2, di2] )
                     
                     images.append( [el2[0], el2[1], di ] )
                     images.append( [xi2, yi2+(el2[1]-yi), di2] )
                 elif fi == 2:
                      el = li[0]
                      images.append( [el[0], el[1], di ] )
                      images.append( [xi2+(el[0]-xi), yi2, di2] )
                 elif fi == 3:
                      el = li[0]
                      images.append( [el[0], el[1], di ] )
                      images.append( [xi2, yi2+(el[1]-yi), di2] )


             
             for j in range(self.N_):
                 xj = self.get_X(j)
                 yj = self.get_Y(j)
                 dj = self.get_D(j)
                 if j-i == 1 and i%2 == 0:
                     bonds.append([xi,yi,xj,yj])
     
                 elif  j > i:
                     
                     dx = xi-xj 
                     dy = yi-yj 
                     dij = di+dj
                     rij2 = dx*dx + dy*dy
                     if rij2 < dij*dij:
                          contacts.append( [xi,yi,xj,yj] )
       
         for i in range(len(images)):
             xi = images[i][0]
             yi = images[i][1]
             di = images[i][2]
             for j in range(len(images)):
                 xj = images[j][0]
                 yj = images[j][1]
                 dj = images[j][2]

                 if j-i == 1 and i%2 == 0:
                     bonds.append([xi,yi,xj,yj])
                 else: #if j > i:
                     dx = xi-xj 
                     dy = yi-yj 
                     dij = di+dj
                     rij2 = dx*dx + dy*dy
                     if rij2 < dij*dij:
                          contacts.append( [xi,yi,xj,yj] )

         for i in range(len(images)):
             xi = images[i][0]
             yi = images[i][1]
             di = images[i][2]
             for j in range(self.N_):
                 xj = self.get_X(j)
                 yj = self.get_Y(j)
                 dj = self.get_D(j)
                 
                 dx = xi-xj 
                 dy = yi-yj 
                 dij = di+dj
                 rij2 = dx*dx + dy*dy
                 if rij2 < dij*dij:
                     contacts.append( [xi,yi,xj,yj] )



         return contacts,bonds



