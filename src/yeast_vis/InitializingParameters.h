const int glutInitWindowSizeX = 720;
const int glutInitWindowSizeY = 720;
const int glutInitWindowPositionX = 1;
const int glutInitWindowPositionY = 1;
static GLfloat spin = 1.0;
static GLint bold = 1;
static GLfloat spinstep = 1.0;
int spinstep_last;

const int NMAX = 2048;
const int nframesMAX = 1000;

const double PI = 3.1415926535;

static GLfloat R[NMAX][nframesMAX];
static GLfloat G[NMAX][nframesMAX];
static GLfloat B[NMAX][nframesMAX];

static GLfloat rStep = 1.0;
static GLfloat gStep = 1.0;
static GLfloat bStep = 1.0;

int i, j, file_index, N[nframesMAX], nframes;
float phi, delry[nframesMAX];;
float xread[NMAX][nframesMAX];
float yread[NMAX][nframesMAX];
float thetaread[NMAX][nframesMAX];
float sig1read[NMAX][nframesMAX];
float sig2read[NMAX][nframesMAX];

float xreadPert[NMAX];
float yreadPert[NMAX];
float thetareadPert[NMAX];

int movie;
