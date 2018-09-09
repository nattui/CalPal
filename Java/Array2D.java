// package braven;

import java.io.IOException;
import java.util.Arrays;

public class Array2D {

	public static int hourglassSum(int[][] arr) {

		int[] hourGlass = new int[7];
		int maximumSum = Integer.MIN_VALUE;

		for (int column = 0; column < 4; column++) {
			for (int row = 0; row < 4; row++) {

				hourGlass[0] = arr[column][row];
				hourGlass[1] = arr[column][row + 1];
				hourGlass[2] = arr[column][row + 2];
				hourGlass[3] = arr[column + 1][row + 1];
				hourGlass[4] = arr[column + 2][row];
				hourGlass[5] = arr[column + 2][row + 1];
				hourGlass[6] = arr[column + 2][row + 2];
				
				int temp = hourGlass[0] + hourGlass[1] + hourGlass[2] + hourGlass[3] + hourGlass[4] + hourGlass[5] + hourGlass[6];
				
				if (temp > maximumSum) {
					maximumSum = temp;
				} 
			}
		}
		
		
		return maximumSum;
	
	}

	// Print the 2D Array
	public static void print2D(int[][] array2D) {
		for (int[] row : array2D) {
			System.out.println(Arrays.toString(row));
		}
	}

	public static void main(String[] args) throws IOException {

		int[][] array2D = new int[6][6];

		// 2D Array
		for (int column = 0; column < array2D.length; column++) {
			System.out.println("col: " + column);

			for (int row = 0; row < array2D.length; row++) {
				System.out.println("row:  " + row);
				array2D[column][row] = 1;

			}
			array2D[0][0] = 9;
			array2D[0][5] = 9;
		}

		System.out.println(array2D.length);
		print2D(array2D);

		System.out.println("");
		System.out.println("");
		System.out.println("");
		System.out.println(hourglassSum(array2D));

	}

}
