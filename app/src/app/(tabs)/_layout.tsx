import { Tabs } from "expo-router";
import BottomNav from "@/components/bottom-nav";

export default function TabsLayout() {
    return (
        <Tabs
            tabBar={() => <BottomNav />}
            screenOptions={{ headerShown: false }}
        >
            <Tabs.Screen name="index" options={{ title: "Home" }} />
            <Tabs.Screen name="calendar" options={{ title: "Calendar" }} />
            <Tabs.Screen name="stats" options={{ title: "Stats" }} />
            <Tabs.Screen name="more" options={{ title: "More" }} />
        </Tabs>
    );
}
