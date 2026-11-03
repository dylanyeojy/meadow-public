import { Text, View } from "react-native";
import { HomeIcon } from "@/components/icons";
import { Link } from "expo-router";

export default function HomeScreen() {
    return (
        <View>
            <Text>This is the Home Page</Text>
            <HomeIcon color="green" />
            <Link href="/login">Go to login</Link>
            <Link href="/register">Go to register</Link>
            <Link href="/onboarding/welcome">Go to welcome</Link>
            <Link href="/onboarding/reminders">Go to reminders</Link>
        </View>
    );
}
