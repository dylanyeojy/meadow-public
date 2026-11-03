import { Text, View, StyleSheet, Pressable } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { colors, type } from "@/theme";
import * as icon from "@/components/icons";
import { router, usePathname } from "expo-router";

export default function BottomNav() {
    const insets = useSafeAreaInsets();
    const pathname = usePathname();
    const isHome = pathname === "/";
    const isCalendar = pathname === "/calendar";
    const isStats = pathname === "/stats";
    const isMore = pathname === "/more";

    return (
        <View style={[styles.bar, { paddingBottom: insets.bottom + 9 }]}>
            <Pressable style={styles.item} onPress={() => router.navigate("/")}>
                <icon.HomeIcon color={isHome ? colors.sage : colors.tertiary} />
                <Text style={[styles.label, isHome && styles.labelActive]}>
                    Home
                </Text>
            </Pressable>

            <Pressable
                style={styles.item}
                onPress={() => router.navigate("/calendar")}
            >
                <icon.CalendarIcon
                    color={isCalendar ? colors.sage : colors.tertiary}
                />
                <Text style={[styles.label, isCalendar && styles.labelActive]}>
                    Calendar
                </Text>
            </Pressable>

            <Pressable
                style={styles.item}
                onPress={() => router.push("/check-in")}
            >
                <View style={styles.circle}>
                    <icon.PlusIcon color={colors.surface} size={22} />
                </View>
                <Text style={[styles.label, styles.labelActive]}>Check in</Text>
            </Pressable>

            <Pressable
                style={styles.item}
                onPress={() => router.navigate("/stats")}
            >
                <icon.StatsIcon
                    color={isStats ? colors.sage : colors.tertiary}
                />
                <Text style={[styles.label, isStats && styles.labelActive]}>
                    Stats
                </Text>
            </Pressable>

            <Pressable
                style={styles.item}
                onPress={() => router.navigate("/more")}
            >
                <icon.MoreIcon color={isMore ? colors.sage : colors.tertiary} />
                <Text style={[styles.label, isMore && styles.labelActive]}>
                    More
                </Text>
            </Pressable>
        </View>
    );
}

const styles = StyleSheet.create({
    bar: {
        flexDirection: "row",
        alignItems: "flex-end",
        backgroundColor: colors.surface,
        borderTopWidth: 1,
        borderTopColor: colors.border,
        paddingTop: 9,
        paddingHorizontal: 20,
    },
    item: {
        flex: 1,
        alignItems: "center",
        gap: 4,
        minHeight: 44,
    },
    label: {
        ...type.caption2,
        letterSpacing: 0.1,
        color: colors.muted,
        fontWeight: "500",
    },
    labelActive: {
        color: colors.sage,
        fontWeight: "700",
    },
    circle: {
        width: 42,
        height: 42,
        borderRadius: 999,
        backgroundColor: colors.sage,
        alignItems: "center",
        justifyContent: "center",
    },
});
