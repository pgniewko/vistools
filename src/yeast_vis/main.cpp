#include "Headers.h"
#include "convert.h"
#include "InitializingParameters.h"
#include "FunctionDeclarations.h"
#include "FunctionDefinitions.h"
#include "FunctionDefinitions2.h"
#include <stdlib.h>    /* atoi,  strtod */

int main(int argc, char** argv)
{
    fstream file;
    int c;
    double L;

    movie = 0;

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DEPTH | GLUT_RGBA | GLUT_DOUBLE);
    glutInitWindowSize(glutInitWindowSizeX, glutInitWindowSizeY);
    glutCreateWindow("*** PRESS 's' TO GRAB SCREENSHOT ***");
    glutInitWindowPosition(glutInitWindowPositionX, glutInitWindowPositionY);

    //file.open("/Users/pawel/School/2DGrowth/output/growth/prod_budding_ar1.01_div4_desync0.4_seed1_Lx30.0_Ly30.0_a2.0_att0.0_P0.001.dat", ios::in);

    file.open(argv[1], ios::in);
    nframes = argv[2] ? atoi (argv[2]) : 700;
    L = argv[3] ? strtod (argv[3], NULL) : 10.0;

    if (nframes > nframesMAX)
    {
        nframes = nframesMAX;
    }

    char line[256];

    for (j = 1; j <= nframes; j++)
    {
        delry[j] = 0.0;
//      file.getline(line, 256);
//      std::cout << line << std::endl;
//      continue;
        file >> N[j];

        cout << j << " " << N[j] << endl;

        for (i = 1; i <= N[j]; i++)
        {
            file >> xread[i][j] >> yread[i][j] >> sig1read[i][j] >> c;

            if (c == 1)
            {
                R[i][j] = 0.7578125; //0.0;
                G[i][j] = 0.6953125; //0.0;
                B[i][j] = 0.5000000; //1.0;
            }
            else
            {
                R[i][j] = 0.82;//1.0;
                G[i][j] = 0.82;//0.0;
                B[i][j] = 0.82;//0.0;
            }

            sig1read[i][j] = sig1read[i][j] / 2.0;
            sig2read[i][j] = sig1read[i][j];

            xread[i][j] = xread[i][j] / L + 0.5 ;
            yread[i][j] = yread[i][j] / L + 0.5;
//            std::cout << "x= " << xread[i][j] << " y= " << yread[i][j] << std::endl;
            sig1read[i][j] = sig1read[i][j] / L;
            sig2read[i][j] = sig2read[i][j] / L;
        }
    }

    glutDisplayFunc(drawEllipse2);
    glutReshapeFunc(reshape);
    glutKeyboardFunc(keyboard);
    glutMouseFunc(mouse);
    glutMainLoop();
    return 0;
}
