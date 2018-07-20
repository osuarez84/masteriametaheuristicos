package ga.ssGA;



/* Autor: Omar Suárez */


public class ProblemKnapSack extends Problem {
	
	
	
	public double Evaluate(Individual Indiv){
		return KNAPSACK(Indiv);
		
	}
	
	
	// Private Methods
    // Coeff for fitness function (values of the objects)
	// Need to be filled with the data from the problem
	private static double p[] = { 	360, 83, 59, 130, 431, 67, 230, 52, 93, 125,
			 						670, 892, 600, 38, 48, 147, 78, 256, 63, 17,
			 						120, 164, 432, 35, 92, 110, 22, 42, 50, 323,
			 						514, 28, 87, 73, 78, 15, 26, 78, 210, 36,
			 						85, 189, 274, 43, 33, 10, 19, 389, 276, 312};
	
	// Matrix coeffs for constraints
	private static int r[][] = {	 {	7, 0, 30, 22, 80, 94, 11, 81, 70, 64,
									 	59, 18, 0, 36, 3, 8, 15, 42, 9, 0,
									 	42, 47, 52, 32, 26, 48, 55, 6, 29, 84,
									 	2, 4, 18, 56, 7, 29, 93, 44, 71, 3,
									 	86, 66, 31, 65, 0, 79, 20, 65, 52, 13},
									 {	8, 66, 98, 50, 0, 30, 0, 88, 15, 37,
									 	26, 72, 61, 57, 17, 27, 83, 3, 9, 66,
									 	97, 42, 2, 44, 71, 11, 25, 74, 90, 20,
									 	0, 38, 33, 14, 9, 23, 12, 58, 6, 14,
										78, 0, 12, 99, 84, 31, 16, 7, 33, 20},
									{	3, 74, 88, 50, 55, 19, 0, 6, 30, 62,
										17, 81, 25, 46, 67, 28, 36, 8, 1, 52,
										19, 37, 27, 62, 39, 84, 16, 14, 21, 5,
										60, 82, 72, 89, 16, 5, 29, 7, 80, 97,
										41, 46, 15, 92, 51, 76, 57, 90, 10, 37},
									{	21, 40, 0, 6, 82, 91, 43, 30, 62, 91,
										10, 41, 12, 4, 80, 77, 98, 50, 78, 35,
										7, 1, 96, 67, 85, 4, 23, 38, 2, 57,
										4, 53, 0, 33, 2, 25, 14, 97, 87, 42,
										15, 65, 19, 83, 67, 70, 80, 39, 9, 5},
									{	94, 86, 80, 92, 31, 17, 65, 51, 46, 66,
										44, 3, 26, 0, 39, 20, 11, 6, 55, 70,
										11, 75, 82, 35, 47, 99, 5, 14, 23, 38,
										94, 66, 64, 27, 77, 50, 28, 25, 61, 10,
										30, 15, 12, 24, 90, 25, 39, 47, 98, 83}
                                    };
	
	// Right-hand values for the constraints
	private static int b[] = { 850, 1400, 1500, 400, 1100}; 
	
	// Number of constraints
	private static int N = 5;
    
    // Number of variables (genes)
    private static int var = 50;
    
    // Optimal value
    private static double opt = 6159.0;
	
	private double KNAPSACK (Individual indiv) {
		
		// [1]
		// Compute the fitness
		double f = 0.0;
		
		for(int i = 0; i < CL; i++){
			// Si la variable es 1 (es decir, si ese objeto ha sido seleccionado)
			// sumamos su valor al fitness
			f = f + p[i] * indiv.get_allele(i);
			
		}
		
		// [2]
		// Comprobamos si cumple todas las restricciones
		// en caso contrario efectuamos una penalización
		// sobre la función de fitness y dejamos
		// vivir la solución junto con las otras
		double v = 0.0;
		for(int i = 0; i < N; i++){
			v = 0.0;
			for(int j = 0; j < CL; j++){
				v = v + indiv.get_allele(j) * r[i][j];
			}
			
			if(v > b[i]){
				// No cumple alguna de las restricciones
				// damos un valor 0 a la funci\'on de coste
				f = 0;
				break;
			}
		}
		
		// seteamos el fitness de la solucion
		indiv.set_fitness(f);
		return f;
		
	}
	
	
	
	
	
}