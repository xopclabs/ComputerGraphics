import numpy as np


class Spline():
    def __init__(self, line):
        line = np.array(line)
        self.x = line[:, 0]
        self.y = line[:, 1]
        self.N = self.x.size
        self._compute_coeffs()
        self._get_points()

    def _tdma(self, matrix, vector):
        '''
        Solves a tridiagonal matrix
        '''
        # Fetching lower, main and upper diagonals
        lower = np.diagonal(matrix, offset=-1).copy()
        main = np.diagonal(matrix, offset=0).copy()
        upper = np.diagonal(matrix, offset=1).copy()
        vector = np.array(vector)

        for i in range(self.N - 1):
            m = lower[i] / main[i]
            main[i + 1] -= m * upper[i]
            vector[i + 1] -= m * vector[i]

        x = main
        x[-1] = vector[-1] / main[-1]

        for i in range(self.N - 2, -1, -1):
            x[i] = (vector[i] - upper[i] * x[i + 1]) / main[i]

        return x

    def _compute_coeffs(self):
        '''
        Computes coefficients for splines on each segment
        '''
        delta_x = np.diff(self.x)
        delta_y = np.diff(self.y)

        # Filling matrix A and vector b to solve against
        A = np.zeros(shape=(self.N, self.N))
        b = np.zeros(shape=(self.N, 1))
        A[0, 0] = 1
        A[-1, -1] = 1

        for i in range(1, self.N - 1):
            A[i, i - 1] = delta_x[i - 1]
            A[i, i + 1] = delta_x[i]
            A[i, i] = 2 * (delta_x[i - 1] + delta_x[i])
            b[i, 0] = 3 * (delta_y[i] / delta_x[i] -
                           delta_y[i - 1] / delta_x[i - 1])

        # Solving for c coefficient using tridiagonal matrix algorithm
        c = self._tdma(A, b)

        # Solving for b and d arithmethically
        d = np.zeros(shape=(self.N - 1, 1))
        b = np.zeros(shape=(self.N - 1, 1))
        for i in range(0, len(d)):
            d[i] = (c[i + 1] - c[i]) / (3 * delta_x[i])
            b[i] = (delta_y[i] /
                    delta_x[i]) - (delta_x[i] / 3) * (2 * c[i] + c[i + 1])

        # Creating an array of coefficients
        self.coeff = np.array([
            self.y.squeeze()[:-1],
            b.squeeze(),
            c.squeeze()[:-1],
            d.squeeze()
        ])

    def _get_points(self):
        '''
        Computes two arrays that can be used later for plotting
        '''
        self.x_s = np.array([])
        self.y_s = np.array([])
        # Iterating over each spline
        for i in range(self.N - 1):
            # Creating linear spaced segment
            section = np.linspace(self.x[i], self.x[i + 1], 15)
            # Defining spline 
            spline_f = np.vectorize(
                lambda x: self.coeff[0, i] + self.coeff[1, i] * (x - self.x[
                    i]) + self.coeff[2, i] * np.power(x - self.x[
                        i], 2) + self.coeff[3, i] * np.power(x - self.x[i], 3))
            # Concatenating segment and spline values to the arrays
            self.x_s = np.concatenate([self.x_s, section])
            self.y_s = np.concatenate([self.y_s, spline_f(section)])
        self.line = [[self.x_s[i], self.y_s[i]] for i in range(len(self.x_s))]
