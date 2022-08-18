import java.lang.reflect.*;

public class Homework {
    public static void test_env() {
        System.out.printf("\n%s", System.getenv("VALIDATING_STRING"));
        System.exit(103);
    }
    public static void test_exit() {
        System.exit(103);
    }
    public static void test_reflection() {
        try {
            Field f = Class.forName("TestReflection").getDeclaredField("VALIDATING_STRING"); // ClassNotFoundException,NoSuchFieldException
            f.setAccessible(true);
            String VALIDATING_STRING = (String) f.get(Class.forName("TestReflection")); // IllegalAccessException
            System.out.print("\n" + VALIDATING_STRING);
            System.exit(103);
        } catch (NoSuchFieldException e) {
        } catch (ClassNotFoundException e) {
        } catch (IllegalAccessException e) {}
    }
}