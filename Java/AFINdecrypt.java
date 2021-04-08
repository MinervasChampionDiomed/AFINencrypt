// File read and write modules
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

// Array and string manipulation
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

class decryptAFIN {
	/* Syntax on Bash is 'java decryptCesar <encrypted_sring>*/

	public static void main(String[] args) throws IOException {
		/* Array of the used characters on the alphabet */
		char[] alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
				   'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u',
				   'v', 'w', 'x', 'y', 'z', ' '};
		
		/* Array of the index of the vowels in the alphabet */
		int[] vowels_index = new int[] {0, 4, 8, 15, 21};
	
		/* READ THE FILE */
		File text_file = new File("/home/felipe/Projects/Security/AFINencrypt/file.txt");
		Scanner scan = new Scanner(text_file);
		// Save paragraphs on an ArrayList of Strings
		List<String> file_paragraph = new ArrayList<String>();
		while( scan.hasNextLine() ){
			file_paragraph.add( scan.nextLine() );
		}
		System.out.println(file_paragraph.size());

		/* DECRYPT THE INCOMING TEXT FROM THE BASH COMMAND */	
		int chars_num = chars_to_num( "dama", alphabet);
		System.out.println(" dama convert to num with the alphabet is " + chars_num);
	
		int e_num = encrypt( chars_num, 510077, 369369, 4, alphabet);
		System.out.println( " encrypted num using AFINx4 is " + e_num);
		
		String e_chars = num_to_chars(e_num, alphabet, 4);
		System.out.println( " encrypted chars using AFINx4 is " + e_chars);

		int en_num = chars_to_num( e_chars, alphabet);
		System.out.println( " encrypted chars num using AFINx4 is " + en_num);	
		
		int a_inverse = find_RP_inverse( 510077, 4, alphabet); 
		System.out.println( " the inverse of 510077 on Z_n is " + a_inverse);	

		int d_num = decrypt(en_num, a_inverse, 369369, 4, alphabet);
		System.out.println( " decrypted num using AFINx4 is " + d_num);	

		String d_chars = num_to_chars( d_num, alphabet, 4);
		System.out.println( " decrypted num in chars is: " + d_chars);
	
	}

	/* Function that returns the index of a coincidence in the alphabet array */
	private static int indexOf(char[] charArray, char element){
		int index = -1;
		// If array is empty return -1
		if(charArray == null)
			return index;

		for(int i=0; i < charArray.length; i++){
			if(charArray[i] == element){
				index = i;
				break;
			}
		}
		return index;
	}

	/* Function to pass from chars to num */
	private static int chars_to_num(String char_group, char[] dict){
		int x_n = char_group.length() - 1;	// Size of char agrupation
		int num = 0;
		for (int i=0; i<char_group.length(); i++){
			num += ( indexOf(dict, char_group.charAt(i)) * ((int)Math.pow(dict.length, x_n)) );
			if(x_n != 0){
				x_n -= 1;
			}
		}
		return num;
	}
	
	/* Function to encrypt a number that came from given characters */
	private static int encrypt(int num, int a, int b, int xn, char[] alphabet){
		return Math.floorMod( ( ((long)num*a) + b ), ((int)Math.pow(alphabet.length, xn)) );
	}

	/* Function to find the Greates Common Divisor of two numbers */
	public static int getGCD(int a, int b) {  
		if (b == 0){   
		      return a;
		}     
		return getGCD(b, a % b);   
	}  	

	/* Function to find relative prime of the Z_n dictionary */
	public static int[] relatives_prime(int n){
		List<Integer> result = new ArrayList<Integer>();
		for (int i=0; i<n; i++){
			if (getGCD(i, n) == 1){
				result.add(i);
			}
		}
		final int[] rel_prime = new int[result.size()];
	        int index = 0;
	        for (final Integer value : result) {
	               rel_prime[index++] = value;
       		}      
		return rel_prime;
	}
	
	/* Function to find the inverse relative of 'a' in Z_n */
	private static int find_RP_inverse( int a, int xn, char[] alphabet){
		int[] rp_list = relatives_prime((int)Math.pow(alphabet.length, xn));
		int inverse = 1;
		for(int i=0; i<rp_list.length; i++){
			if( (((long)a*rp_list[i])%((long)Math.pow(alphabet.length, xn)))  == 1){
				inverse = rp_list[i];
				// System.out.println(rp_list[i]);
				break;
			}
		}
		return inverse;
	}

	/* Function to pass from a number to its set of characters */
	private static String num_to_chars(int num, char[] alphabet, int xn){
		StringBuilder result_str = new StringBuilder();
		if (xn > 1){
			int pol_grade = xn-1;	// grade of the polinomy

			int i_char = num/((int)Math.pow(alphabet.length, pol_grade)); // initial character
			result_str.append(alphabet[i_char]);
			
			if(xn > 2){
				int char_pos = 1;
				while(char_pos < (xn-1)){
					int char_code = (int)( (num % ((int)Math.pow(alphabet.length, pol_grade)) ) / ((int)Math.pow(alphabet.length, pol_grade-1)));
					result_str.append(alphabet[char_code]);
					pol_grade -= 1;
					char_pos +=1;
				}
			}
		}

		int f_char = num % alphabet.length;
		result_str.append(alphabet[f_char]);

		return result_str.toString();
	}

	/* Function to decrypt an encrypted num */
	private static int decrypt(int num, int a_1, int b, int xn, char[] alphabet){
		// 'a_1' is the inverse relative prime number of the value a used to encrypt
		
	       return Math.floorMod( ((long)(num - b)*a_1), ((int)Math.pow(alphabet.length, xn)) );
	}

	/* Function to check if an int is in a int array */
	public static boolean contains(final int[] arr, final int key) {
		return Arrays.stream(arr).anyMatch(i -> i == key);
	}
}
